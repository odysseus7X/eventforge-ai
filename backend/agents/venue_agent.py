from backend.state import ConferenceState

async def run_venue_agent(state: ConferenceState) -> dict:
    """
    Reads:  state["conference_input"]  (geography, audience_size, budget_usd)
    Writes: {"venues": VenueAgentOutput}

    Steps:
        1. Call query_venues(geography, min_capacity=audience_size)
        2. Call call_llm(..., response_model=VenueAgentOutput)
           Ask Claude to rank and explain venue recommendations
        3. Return {"venues": result}
    """
    ...