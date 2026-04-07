from backend.state import ConferenceState

async def run_speaker_agent(state: ConferenceState) -> dict:
    """
    Reads:  state["conference_input"]
    Writes: {"speakers": SpeakerAgentOutput}

    Steps:
        1. Get category, geography from state["conference_input"]
        2. Call search_web() with query like "top {category} speakers {geography} 2025"
        3. Also call query_past_events() for historical speaker context
        4. Call call_llm(..., response_model=SpeakerAgentOutput)
        5. Return {"speakers": result}

    Only agent that uses web_search tool.
    """
    ...