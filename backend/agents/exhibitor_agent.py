from backend.state import ConferenceState

async def run_exhibitor_agent(state: ConferenceState) -> dict:
    """
    Reads:  state["conference_input"]
    Writes: {"exhibitors": ExhibitorAgentOutput}

    Steps:
        1. Call query_past_events() for exhibitor data in past events
        2. Call call_llm(..., response_model=ExhibitorAgentOutput)
           Ask Claude to cluster and recommend exhibitors by type
        3. Return {"exhibitors": result}
    """
    ...