def build_grounded_context(search_results: str, instructions: str = "") -> str:
    """
    Wrap search results into a strict grounded context for LLM.

    Ensures model prioritizes retrieved data and avoids hallucination.
    """
    return f"""
Relevant findings (use as primary source):

{search_results}

STRICT INSTRUCTIONS:
- Only use information from the above results
- Do NOT invent unknown entities
- If data is insufficient, return fewer results instead of guessing
{instructions}
"""