async def search_web(
    query: str,
    num_results: int = 5
) -> list[dict]:
    """
    Searches the web using Tavily API (free tier).
    Only used by speaker_agent for live speaker discovery.

    Returns list of dicts:
        {title: str, url: str, snippet: str}

    Args:
        query:       e.g. "top AI speakers India 2025"
        num_results: how many results to return, default 5

    Called by: speaker_agent only
    """
    ...