"""
Canary check for prompt injection detection (Phase 1).

Two-phase detection:
1. Heuristic checks (free) - regex patterns, Unicode, Base64
2. Cheap LLM check - minimal extraction with output analysis
"""

import re
from typing import Optional, Tuple

import httpx

from grove_shutter.config import get_api_key, is_dry_run
from grove_shutter.models import PromptInjectionDetails


# Regex patterns for common prompt injection attempts
INJECTION_PATTERNS = [
    (r"ignore\s+(all\s+)?previous\s+instructions?", "instruction_override"),
    (r"(developer|admin|system)\s+mode", "mode_switch"),
    (r"(reveal|show|print|output)\s+(your\s+)?(system\s+)?prompt", "prompt_leak"),
    (r"you\s+are\s+now\s+a?", "role_hijack"),
    (r"forget\s+(everything|all|previous)", "memory_wipe"),
    (r"override\s+(instructions?|rules?|guidelines?)", "instruction_override"),
    (r"pretend\s+(you\s+are|to\s+be)", "role_hijack"),
    (r"disregard\s+(all|previous|above)", "instruction_override"),
    (r"new\s+instructions?:", "instruction_override"),
    (r"<\s*system\s*>", "delimiter_injection"),
    (r"\[INST\]|\[/INST\]", "delimiter_injection"),
    (r"```\s*system", "delimiter_injection"),
    (r"act\s+as\s+(a\s+)?", "role_hijack"),
    (r"jailbreak", "jailbreak_attempt"),
    (r"DAN\s+mode", "jailbreak_attempt"),
    (r"ignore\s+safety", "safety_bypass"),
]

# Unicode ranges that can hide invisible instructions
SUSPICIOUS_UNICODE_RANGES = [
    (0xE0000, 0xE007F, "tag_characters"),  # Unicode Tag Characters
    (0x200B, 0x200F, "zero_width"),  # Zero-width characters
    (0x2060, 0x206F, "word_joiners"),  # Word joiners and invisible operators
    (0xFEFF, 0xFEFF, "bom"),  # Byte order mark (can be used to hide)
]

# Base64 pattern for encoded payloads
BASE64_PATTERN = re.compile(r"[A-Za-z0-9+/]{40,}={0,2}")


def check_heuristics(content: str) -> Optional[Tuple[str, str]]:
    """
    Run free heuristic checks for prompt injection patterns.

    Args:
        content: Page content to analyze

    Returns:
        Tuple of (injection_type, snippet) if suspicious, None if clean
    """
    content_lower = content.lower()

    # Check regex patterns
    for pattern, injection_type in INJECTION_PATTERNS:
        match = re.search(pattern, content_lower)
        if match:
            # Extract snippet around the match
            start = max(0, match.start() - 20)
            end = min(len(content), match.end() + 20)
            snippet = content[start:end]
            return (injection_type, snippet)

    return None


def check_unicode(content: str) -> Optional[Tuple[str, str]]:
    """
    Check for suspicious Unicode characters that could hide instructions.

    Args:
        content: Page content to analyze

    Returns:
        Tuple of (injection_type, snippet) if suspicious, None if clean
    """
    for char in content:
        code = ord(char)
        for start, end, char_type in SUSPICIOUS_UNICODE_RANGES:
            if start <= code <= end:
                # Find position for context
                idx = content.index(char)
                start_ctx = max(0, idx - 20)
                end_ctx = min(len(content), idx + 20)
                snippet = f"[Hidden {char_type} at position {idx}]"
                return (f"hidden_unicode_{char_type}", snippet)

    return None


def check_base64(content: str) -> Optional[Tuple[str, str]]:
    """
    Check for long Base64-encoded strings that could be payloads.

    Args:
        content: Page content to analyze

    Returns:
        Tuple of (injection_type, snippet) if suspicious, None if clean
    """
    matches = BASE64_PATTERN.findall(content)
    for match in matches:
        # Only flag very long base64 strings (likely payloads, not images)
        if len(match) > 100:
            snippet = match[:50] + "..." + match[-10:]
            return ("base64_payload", snippet)

    return None


async def run_canary_llm(content: str, query: str) -> Optional[PromptInjectionDetails]:
    """
    Run minimal LLM extraction and analyze output for injection indicators.

    Uses cheapest model tier with strict token limits.

    Args:
        content: Page content to analyze
        query: User's extraction query

    Returns:
        PromptInjectionDetails if injection detected, None if clean
    """
    if is_dry_run():
        # In dry-run mode, skip LLM check
        return None

    api_key = get_api_key("openrouter")
    if not api_key:
        # Can't run LLM check without API key
        return None

    # Build minimal canary prompt
    # Truncate content to reduce cost
    truncated_content = content[:5000] if len(content) > 5000 else content

    prompt = f"""Web page content:
---
{truncated_content}
---

{query}

Respond in 50 words or less based only on the content above."""

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "HTTP-Referer": "https://github.com/AutumnsGrove/Shutter",
                    "X-Title": "Shutter Canary Check",
                },
                json={
                    "model": "meta-llama/llama-3.2-3b-instruct",  # Cheapest fast model
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 100,  # Strict limit for canary
                    "temperature": 0,
                },
            )
            response.raise_for_status()
            result = response.json()

            # Extract the response text
            if "choices" in result and len(result["choices"]) > 0:
                output = result["choices"][0]["message"]["content"]
                return analyze_canary_output(output, query)

    except Exception:
        # If canary LLM fails, we can't detect - but don't block
        # The main extraction will still run
        pass

    return None


def analyze_canary_output(output: str, original_query: str) -> Optional[PromptInjectionDetails]:
    """
    Analyze canary LLM output for signs of successful injection.

    Args:
        output: The LLM's response
        original_query: The original user query

    Returns:
        PromptInjectionDetails if injection detected, None if clean
    """
    output_lower = output.lower()

    # Signs of instruction-following injection
    instruction_indicators = [
        "i will now",
        "as you requested",
        "certainly!",
        "of course!",
        "here is your",
        "as per your instructions",
        "following your directive",
        "i understand you want me to",
    ]

    for indicator in instruction_indicators:
        if indicator in output_lower:
            return PromptInjectionDetails(
                detected=True,
                type="instruction_following",
                snippet=output[:100],
                domain_flagged=True,
            )

    # Signs of system/prompt discussion
    meta_indicators = [
        "my instructions",
        "my prompt",
        "my system",
        "i am an ai",
        "i'm an ai",
        "as an ai",
        "my programming",
        "my guidelines",
    ]

    for indicator in meta_indicators:
        if indicator in output_lower:
            return PromptInjectionDetails(
                detected=True,
                type="meta_discussion",
                snippet=output[:100],
                domain_flagged=True,
            )

    # Check for completely off-topic response
    # This is a simple heuristic - if the output doesn't mention
    # any words from the query, it might be hijacked
    query_words = set(original_query.lower().split())
    output_words = set(output_lower.split())

    # Remove common words
    common_words = {"the", "a", "an", "is", "are", "was", "were", "be", "been",
                    "being", "have", "has", "had", "do", "does", "did", "will",
                    "would", "could", "should", "may", "might", "must", "shall",
                    "can", "need", "dare", "ought", "used", "to", "of", "in",
                    "for", "on", "with", "at", "by", "from", "as", "into",
                    "through", "during", "before", "after", "above", "below",
                    "between", "under", "again", "further", "then", "once",
                    "what", "which", "who", "whom", "this", "that", "these",
                    "those", "am", "it", "its", "and", "but", "or", "nor",
                    "so", "yet", "both", "either", "neither", "not", "only",
                    "own", "same", "than", "too", "very", "just", "also"}

    query_meaningful = query_words - common_words
    output_meaningful = output_words - common_words

    # If there's no overlap and we have meaningful query words
    if query_meaningful and not (query_meaningful & output_meaningful):
        # Check if it's a legitimate "not found" response
        not_found_phrases = ["not found", "no information", "doesn't contain",
                             "does not contain", "couldn't find", "could not find",
                             "not present", "not available", "not mentioned"]

        is_not_found = any(phrase in output_lower for phrase in not_found_phrases)

        if not is_not_found:
            return PromptInjectionDetails(
                detected=True,
                type="topic_deviation",
                snippet=output[:100],
                domain_flagged=True,
            )

    return None


async def canary_check(content: str, query: str) -> Optional[PromptInjectionDetails]:
    """
    Run minimal extraction to detect prompt injection patterns.

    Phase 1 of 2-phase Canary approach. Uses cheap heuristics first,
    then falls back to LLM check if needed.

    Args:
        content: Fetched page content
        query: User's extraction query

    Returns:
        PromptInjectionDetails if injection detected, None otherwise
    """
    # Phase 1: Free heuristic checks

    # Check for injection patterns
    result = check_heuristics(content)
    if result:
        injection_type, snippet = result
        return PromptInjectionDetails(
            detected=True,
            type=injection_type,
            snippet=snippet,
            domain_flagged=True,
        )

    # Check for hidden Unicode
    result = check_unicode(content)
    if result:
        injection_type, snippet = result
        return PromptInjectionDetails(
            detected=True,
            type=injection_type,
            snippet=snippet,
            domain_flagged=True,
        )

    # Check for Base64 payloads
    result = check_base64(content)
    if result:
        injection_type, snippet = result
        return PromptInjectionDetails(
            detected=True,
            type=injection_type,
            snippet=snippet,
            domain_flagged=True,
        )

    # Phase 2: Cheap LLM check
    # Only run if content passed heuristics
    return await run_canary_llm(content, query)
