# from langchain_core.tools import tool


# @tool
# async def search_sponsors(query: str) -> str:
#     """
#     Search for companies that sponsor conferences.
#     Input should include category and geography.
#     """
#     # Replace later with real API (SerpAPI, Tavily, etc.)
#     return f"""
#     Potential sponsors for {query}:
#     - AWS (Cloud, frequent AI conference sponsor)
#     - NVIDIA (AI hardware, major sponsor)
#     - Google (AI + Cloud)
#     - Microsoft (Azure, enterprise AI)
#     """


# @tool
# async def search_speakers(query: str) -> str:
#     """
#     Search for relevant conference speakers.
#     Input should include category and geography.
#     """
#     return f"""
#     Potential speakers for {query}:
#     - Andrew Ng (AI educator, founder of DeepLearning.AI)
#     - Fei-Fei Li (Stanford, AI + vision leader)
#     - Demis Hassabis (DeepMind CEO)
#     - Jensen Huang (NVIDIA CEO, AI hardware)
#     - Sundar Pichai (Google CEO, AI strategy)
#     """

# @tool
# async def search_venues(query: str) -> str:
#     """
#     Search for suitable conference venues.
#     Input should include category, geography, and audience size context.
#     Returns a list of venues with approximate capacity and relevance.
#     """
#     return f"""
#     Possible venues for {query}:
#     - Bangalore International Convention Centre (capacity 5000)
#     - Jio World Convention Centre (Mumbai, premium venue)
#     - Pragati Maidan (Delhi, large expo space)
#     - HITEX Hyderabad (tech conferences)
#     """

from dotenv import load_dotenv
from langchain_core.tools import tool
from tavily import TavilyClient
import os
import asyncio


load_dotenv()

client = TavilyClient(api_key="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")


async def _search(query: str, max_results: int = 5) -> str:
    """
    Internal async wrapper for Tavily search
    """
    loop = asyncio.get_event_loop()

    response = await loop.run_in_executor(
        None,
        lambda: client.search(
            query=query,
            max_results=max_results,
            search_depth="advanced"
        )
    )

    results = response.get("results", [])

    # clean text summary for LLM
    formatted = []
    for r in results:
        title = r.get("title", "")
        content = r.get("content", "")
        formatted.append(f"- {title}: {content[:200]}")

    return "\n".join(formatted)


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
    return await _search(f"{query} sponsors companies AI events")


@tool
async def search_speakers(query: str) -> str:
    """
    Search for relevant conference speakers.
    Input:
        query: Should include category and geography.
    
    Returns:
        A concise list of relevant sponsor companies with brief descriptions.
    """
    return await _search(f"{query} top speakers AI conference")


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