from backend.state import ConferenceState

async def run_gtm_agent(state: ConferenceState) -> dict:
    """
    Reads:  state["conference_input"]  (category, geography)
    Writes: {"gtm": GTMAgentOutput}

    Steps:
        1. Call query_communities(category, geography)
        2. Call call_llm(..., response_model=GTMAgentOutput)
           Give Claude the community list, ask it to generate
           promotion messages and a distribution plan
        3. Return {"gtm": result}
    """
    ...