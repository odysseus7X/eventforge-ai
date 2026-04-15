from eventforge.tools.web_search import web_search
from eventforge.tools.vector_store import retrieve_similar_events

TOOLS = [
    web_search,
    retrieve_similar_events
]