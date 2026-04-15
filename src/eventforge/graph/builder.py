from langgraph.graph import StateGraph, START, END

from eventforge.agents.pricing_agent import PricingAgent
from eventforge.agents.venue_agent import VenueAgent
from eventforge.models.state import ConferenceState
from eventforge.agents.sponsor_agent import SponsorAgent
from eventforge.agents.speaker_agent import SpeakerAgent
from eventforge.agents.final_agent import FinalAgent

async def join_node(state: ConferenceState) -> dict:
    """Barrier node: waits for all upstream nodes."""
    return {}

def build_graph():
    graph = StateGraph(ConferenceState)

    sponsor = SponsorAgent()
    speaker = SpeakerAgent()
    venue = VenueAgent()
    pricing = PricingAgent()
    final = FinalAgent()

    # ---- Nodes ----
    graph.add_node("sponsor_agent", sponsor.run)
    graph.add_node("speaker_agent", speaker.run)
    graph.add_node("venue_agent", venue.run)
    graph.add_node("pricing_agent", pricing.run)
    # graph.add_node("join", join_node)
    graph.add_node("final_agent", final.run)

    # ---- parallel start ----
    graph.add_edge(START, "sponsor_agent")
    graph.add_edge(START, "speaker_agent")
    graph.add_edge(START, "venue_agent")
    
    # ---- dependency ----
    graph.add_edge("venue_agent", "pricing_agent")

    graph.add_edge(
        ["sponsor_agent", "speaker_agent", "pricing_agent"],
        "final_agent"
    )
    
    
    # ---- convergence ----
    # graph.add_edge("sponsor_agent", "join")
    # graph.add_edge("speaker_agent", "join")
    # graph.add_edge("venue_agent", "join")
    # graph.add_edge("pricing_agent", "join")

    # graph.add_edge("join", "final_agent")

    # ---- End ----
    graph.add_edge("final_agent", END)

    return graph.compile()