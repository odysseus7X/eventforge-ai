from langchain_core.tools import tool


@tool
async def search_sponsors(query: str) -> str:
    """
    Search for companies that sponsor conferences.
    Input should include category and geography.
    """
    # Replace later with real API (SerpAPI, Tavily, etc.)
    return f"""
    Potential sponsors for {query}:
    - AWS (Cloud, frequent AI conference sponsor)
    - NVIDIA (AI hardware, major sponsor)
    - Google (AI + Cloud)
    - Microsoft (Azure, enterprise AI)
    """


@tool
async def search_speakers(query: str) -> str:
    """
    Search for relevant conference speakers.
    Input should include category and geography.
    """
    return f"""
    Potential speakers for {query}:
    - Andrew Ng (AI educator, founder of DeepLearning.AI)
    - Fei-Fei Li (Stanford, AI + vision leader)
    - Demis Hassabis (DeepMind CEO)
    - Jensen Huang (NVIDIA CEO, AI hardware)
    - Sundar Pichai (Google CEO, AI strategy)
    """

@tool
async def search_venues(query: str) -> str:
    """
    Search for suitable conference venues.
    Input should include category, geography, and audience size context.
    Returns a list of venues with approximate capacity and relevance.
    """
    return f"""
    Possible venues for {query}:
    - Bangalore International Convention Centre (capacity 5000)
    - Jio World Convention Centre (Mumbai, premium venue)
    - Pragati Maidan (Delhi, large expo space)
    - HITEX Hyderabad (tech conferences)
    """
