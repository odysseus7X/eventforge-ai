import asyncio

from eventforge.graph.builder import build_graph
from eventforge.utils.logging import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)


async def main():
    graph = build_graph()

    # 🔥 TAKE USER INPUT
    category = input("Enter conference category: ")
    geography = input("Enter geography: ")
    audience_size = int(input("Enter audience size: "))

    state = {
        "input": {
            "category": category,
            "geography": geography,
            "audience_size": audience_size
        },
        "outputs": {},
        "agent_meta": {},
        "shared_memory": {},
        "logs": [],
        "errors": []
    }

    logger.info("Starting EventForge pipeline...")

    # 🔥 STREAM (optional but nice)
    async for chunk in graph.astream(state):
        logger.debug(f"Update: {chunk}")

    result = await graph.ainvoke(state)

    logger.info("Graph execution completed")

    print("\n=== FINAL OUTPUT ===\n")
    print(result["outputs"]["final_agent"])


if __name__ == "__main__":
    asyncio.run(main())