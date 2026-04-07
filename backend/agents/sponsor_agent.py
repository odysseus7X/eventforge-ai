from backend.state import ConferenceState

async def run_sponsor_agent(state: ConferenceState) -> dict:
    """
    Reads:  state["conference_input"]
    Writes: {"sponsors": SponsorAgentOutput}

    Steps:
        1. Get category, geography from state["conference_input"]
        2. Call query_past_events() and query_sponsors() from vector_store
        3. Build system_prompt + user_prompt with that context
        4. Call call_llm(..., response_model=SponsorAgentOutput)
        5. Return {"sponsors": result}

    Returns dict with key "sponsors" — LangGraph merges this into state
    """
    ...