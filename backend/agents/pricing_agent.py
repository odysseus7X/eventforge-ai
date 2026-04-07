from backend.state import ConferenceState

async def run_pricing_agent(state: ConferenceState) -> dict:
    """
    Reads:  state["conference_input"]  (audience_size, budget_usd, category)
    Writes: {"pricing": PricingAgentOutput}

    Steps:
        1. Call query_past_events() to get historical ticket prices
           and attendance numbers for similar events
        2. Call call_llm(..., response_model=PricingAgentOutput)
           Give Claude the historical data, ask it to recommend
           pricing tiers and predict attendance + revenue
        3. Return {"pricing": result}

    Note: No ML model needed — Claude reasons over historical data directly.
    The notebooks/pricing_model.ipynb is optional bonus work.
    """
    ...