"""
HTTP fetching with httpx and optional Tavily enhancement.
"""

import httpx
import trafilatura
from typing import Optional

from grove_shutter.config import get_api_key


class FetchError(Exception):
    """Raised when URL fetching fails."""

    def __init__(self, url: str, reason: str):
        self.url = url
        self.reason = reason
        super().__init__(f"Failed to fetch {url}: {reason}")


async def fetch_url(url: str, timeout: int = 30000) -> str:
    """
    Fetch URL content using httpx and extract clean text.

    Args:
        url: URL to fetch
        timeout: Timeout in milliseconds

    Returns:
        Extracted text content (markdown-like format)

    Raises:
        FetchError: If fetching or extraction fails
    """
    timeout_seconds = timeout / 1000

    try:
        async with httpx.AsyncClient(
            timeout=timeout_seconds,
            follow_redirects=True,
            headers={
                "User-Agent": "Shutter/0.1 (Web Content Distillation Service)"
            }
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
            html = response.text
    except httpx.TimeoutException:
        raise FetchError(url, "Request timed out")
    except httpx.HTTPStatusError as e:
        raise FetchError(url, f"HTTP {e.response.status_code}")
    except httpx.RequestError as e:
        raise FetchError(url, str(e))

    # Extract clean text from HTML using trafilatura
    extracted = html_to_text(html)
    if not extracted:
        raise FetchError(url, "Could not extract content from page")

    return extracted


def html_to_text(html: str) -> Optional[str]:
    """
    Convert HTML to clean text using trafilatura.

    Removes navigation, ads, boilerplate content and extracts
    main article content in a readable format.

    Args:
        html: Raw HTML content

    Returns:
        Extracted text content, or None if extraction fails
    """
    # trafilatura.extract returns clean text/markdown
    # include_comments=False to avoid potential injection vectors
    # include_tables=True to preserve tabular data
    extracted = trafilatura.extract(
        html,
        include_comments=False,
        include_tables=True,
        include_links=False,  # Links often add noise
        output_format="txt",  # Plain text is sufficient
        deduplicate=True,
    )
    return extracted


async def fetch_with_tavily(url: str, query: str) -> str:
    """
    Enhanced fetch using Tavily SDK for JavaScript-rendered content.

    Falls back to basic fetch if Tavily API key is not available.

    Args:
        url: URL to fetch
        query: Context for enhanced extraction

    Returns:
        Enhanced page content

    Raises:
        FetchError: If fetching fails
    """
    tavily_key = get_api_key("tavily")

    if not tavily_key:
        # Fall back to basic fetch if no Tavily key
        return await fetch_url(url)

    try:
        from tavily import TavilyClient

        client = TavilyClient(api_key=tavily_key)

        # Use Tavily extract for single URL
        result = client.extract(urls=[url])

        if result and "results" in result and len(result["results"]) > 0:
            # Return the raw content from Tavily
            content = result["results"][0].get("raw_content", "")
            if content:
                return content

        # Fall back if Tavily returned no content
        return await fetch_url(url)

    except ImportError:
        # tavily-python not installed, fall back
        return await fetch_url(url)
    except Exception:
        # Any Tavily error, fall back to basic fetch
        return await fetch_url(url)


def extract_domain(url: str) -> str:
    """
    Extract domain from URL for offenders list tracking.

    Args:
        url: Full URL

    Returns:
        Domain name (e.g., "example.com")
    """
    from urllib.parse import urlparse

    parsed = urlparse(url)
    domain = parsed.netloc

    # Remove www. prefix for consistency
    if domain.startswith("www."):
        domain = domain[4:]

    # Remove port if present
    if ":" in domain:
        domain = domain.split(":")[0]

    return domain
