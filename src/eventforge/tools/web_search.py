from langchain_core.tools import tool
from tavily import TavilyClient
import os
import asyncio
from eventforge.utils.llm_client import _get_env

client = TavilyClient(api_key=_get_env("TAVILY_API_KEY"))


def _clean_results(results):
    cleaned = []

    for r in results:
        title = r.get("title", "").strip()
        content = r.get("content", "").strip()

        # filters
        if not title or not content:
            continue
        if len(content) < 80:
            continue
        if any(x in title.lower() for x in ["login", "signup", "advertisement"]):
            continue

        cleaned.append(f"- {title}: {content[:200]}")

    return cleaned


async def _search(query: str, max_results: int = 5) -> str:
    """
    Internal async wrapper for Tavily search
    """
    loop = asyncio.get_event_loop()

    response = await loop.run_in_executor(
        None,
        lambda: client.search(
            query=query, max_results=max_results, search_depth="advanced"
        ),
    )

    results = response.get("results", [])

    cleaned = _clean_results(results)

    return "\n".join(cleaned[:5])


# ─────────────────────────────────────────────
# TOOLS
# ─────────────────────────────────────────────


@tool
async def search_sponsors(query: str) -> str:
    """
    Search for companies that sponsor conferences.
    Input:
        query: Should include category and geography.

    Returns:
        A concise list of relevant sponsor companies with brief descriptions.
    """
    return await _search(f"{query} sponsors companies")


@tool
async def search_speakers(query: str) -> str:
    """
    Search for relevant conference speakers.
    Input:
        query: Should include category and geography.

    Returns:
        A concise list of relevant sponsor companies with brief descriptions.
    """
    return await _search(f"{query} top speakers")


@tool
async def search_venues(query: str) -> str:
    """
    Search for suitable conference venues.
    Input:
        query: Should include category, geography, and audience size context.

    Returns:
        A concise text summary of relevant venues, including names,
        capacities, and key details.
    """
    return await _search(f"{query} large conference venues capacity")


@tool
async def search_exhibitors(query: str) -> str:
    """
    Search for companies that exhibit at conferences.
    Input:
        query: Should include category and geography.

    Returns:
        A concise list of relevant exhibitor companies with brief descriptions.
    """
    return await _search(
        f"{query} conference exhibitors companies startup tools booths"
    )


@tool
async def search_communities(query: str) -> str:
    """
    Search for communities where the event can be promoted.
    Input:
        query: Should include category and geography.

    Returns:
        A concise list of relevant online communities (Discord, LinkedIn, Meetup, etc.)
        suitable for promoting the event.
    """
    return await _search(
        f"{query} communities discord linkedin meetup groups"
    )
