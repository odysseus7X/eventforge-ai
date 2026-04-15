# from pathlib import Path
# from typing import Any, Dict, Mapping, Sequence

# import chromadb
# from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# BASE_DIR = Path(__file__).resolve().parent.parent
# CHROMA_PATH = BASE_DIR / "data" / "chroma_db"

# _client = chromadb.PersistentClient(
#     path=str(CHROMA_PATH)
# )  # Module-level Chroma client — initialized once on import
# _events_collection: chromadb.Collection
# _communities_collection: chromadb.Collection
# _embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")


# def get_events_collection() -> chromadb.Collection:
#     """
#     Returns the Chroma collection for past events.
#     Creates it if it doesn't exist yet.
#     Called by: data_loader.py, and all query functions below
#     """
#     global _events_collection

#     if _events_collection is None:
#         _events_collection = _client.get_or_create_collection(
#             name="events,", embedding_function=_embedding_fn
#         )

#     return _events_collection


# def get_communities_collection() -> chromadb.Collection:
#     """
#     Returns the Chroma collection for communities/discord servers.
#     Creates it if it doesn't exist yet.
#     Called by: data_loader.py, query_communities()
#     """
#     global _communities_collection

#     if _communities_collection is None:
#         _communities_collection = _client.get_or_create_collection(
#             name="communities", embedding_function=_embedding_fn
#         )

#     return _communities_collection


# async def query_past_events(
#     category: str, geography: str, top_k: int = 10
# ) -> Sequence[Mapping[str, Any]]:
#     """
#     Semantic search over past events dataset.
#     Finds events most similar to the given category + geography.

#     Returns list of dicts, each dict is one CSV row:
#         {event_name, location, category, sponsors, speakers,
#          exhibitors, ticket_price_usd, estimated_attendance, year}

#     Called by: sponsor_agent, speaker_agent, exhibitor_agent, pricing_agent
#     """
#     collection = get_events_collection()

#     query = f"{category} conference in {geography}"

#     results = collection.query(
#         query_texts=[query],
#         n_results=top_k,
#     )
#     metadatas = results.get("metadatas")
#     if not metadatas:
#         return []
#     return metadatas[0]


# async def query_sponsors(category: str, geography: str, top_k: int = 15) -> list[dict]:
#     """
#     Focused search for past sponsor data only.
#     Extracts and returns sponsor-specific info from events collection.

#     Returns list of dicts:
#         {sponsor_name, event_name, category, geography, year}

#     Called by: sponsor_agent
#     """
#     events = await query_past_events(category, geography, top_k)
    
#     sponsors = []

#     for e in events:
#         if "sponsors" in e:
#             for s in e["sponsors"].split(","):
#                 sponsors.append({
#                     "sponsor_name": s.strip(),
#                     "event_name": e.get("event_name"),
#                     "category": e.get("category"),
#                     "geography": e.get("location"),
#                     "year": e.get("year")
#                 })

#     return sponsors


# async def query_venues(
#     geography: str, min_capacity: int, top_k: int = 10
# ) -> list[dict]:
#     """
#     Search for venues matching geography and capacity requirement.

#     Returns list of dicts:
#         {venue_name, city, capacity, price_per_day_usd, past_events}

#     Called by: venue_agent
#     """
#     collection = get_events_collection()

#     query = f"venues in {geography} capacity {min_capacity}"

#     results = collection.query(
#         query_texts=[query],
#         n_results=top_k
#     )

#     venues = []

#     for m in results["metadatas"][0]:
#         if m.get("capacity", 0) >= min_capacity:
#             venues.append({
#                 "venue_name": m.get("venue_name"),
#                 "city": m.get("location"),
#                 "capacity": m.get("capacity"),
#                 "price_per_day_usd": m.get("price_per_day_usd"),
#                 "past_events": m.get("past_events", [])
#             })

#     return venues


# async def query_communities(
#     category: str, geography: str, top_k: int = 20
# ) -> list[dict]:
#     """
#     Search communities dataset for relevant Discord/Slack/Reddit groups.

#     Returns list of dicts:
#         {community_name, platform, niche, member_count, geography}

#     Called by: gtm_agent
#     """
#     collection = get_communities_collection()
    
#     query = f"{category} community in {geography}"
    
#     results = collection.query(
#         query_texts=[query],
#         n_results=top_k
#     )
    
#     return results["metadatas"][0]


from langchain_core.tools import tool

@tool
def retrieve_similar_events(query: str) -> str:
    """
    Retrieve similar past events from vector DB.
    """
    return f"Mock vector results for: {query}"