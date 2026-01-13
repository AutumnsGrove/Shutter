"""
Full extraction logic (Phase 2) - runs only if Canary passes.
"""

from typing import Tuple


async def extract_content(
    content: str,
    query: str,
    model: str = "fast",
    max_tokens: int = 500,
    extended_query: str = None,
) -> Tuple[str, int, int, str]:
    """
    Run full LLM extraction on page content.

    Phase 2 of 2-phase approach. Only runs if Phase 1 (Canary) passes.

    Args:
        content: Fetched page content
        query: What to extract
        model: Model preference (fast/accurate/research/code)
        max_tokens: Maximum output tokens
        extended_query: Additional extraction instructions

    Returns:
        Tuple of (extracted_text, tokens_input, tokens_output, model_used)
    """
    # TODO: Implement extraction via OpenRouter
    pass


def get_model_for_tier(tier: str) -> str:
    """
    Map model tier to actual OpenRouter model.

    Args:
        tier: One of fast/accurate/research/code

    Returns:
        OpenRouter model identifier
    """
    model_map = {
        "fast": "cerebras/llama-3.3-70b",  # or groq/fastest
        "accurate": "deepseek/deepseek-chat",
        "research": "qwen/qwen-3-30b",
        "code": "minimax/m2.1",
    }
    return model_map.get(tier, model_map["fast"])
