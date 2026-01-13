"""
Core shutter() function - main entry point for the distillation service.
"""

from typing import Optional
from grove_shutter.models import ShutterRequest, ShutterResponse


async def shutter(
    url: str,
    query: str,
    model: str = "fast",
    max_tokens: int = 500,
    extended_query: Optional[str] = None,
    timeout: int = 30000,
) -> ShutterResponse:
    """
    Fetch and distill web content through LLM extraction.

    Args:
        url: URL to fetch
        query: What to extract from the page
        model: Model preference (fast/accurate/research/code)
        max_tokens: Maximum output tokens
        extended_query: Additional extraction instructions
        timeout: Fetch timeout in milliseconds

    Returns:
        ShutterResponse with extracted content or prompt injection details
    """
    # TODO: Implement core shutter logic
    pass
