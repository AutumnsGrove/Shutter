"""
Canary check for prompt injection detection (Phase 1).
"""

from typing import Optional
from grove_shutter.models import PromptInjectionDetails


async def canary_check(content: str, query: str) -> Optional[PromptInjectionDetails]:
    """
    Run minimal extraction to detect prompt injection patterns.

    Phase 1 of 2-phase Canary approach. Uses cheap LLM with 100-200 tokens
    to check for instruction-override patterns.

    Args:
        content: Fetched page content
        query: User's extraction query

    Returns:
        PromptInjectionDetails if injection detected, None otherwise
    """
    # TODO: Implement canary check logic
    pass
