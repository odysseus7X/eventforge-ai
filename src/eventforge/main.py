import asyncio

from eventforge.graph.builder import build_graph
from eventforge.utils.logging import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)

async def main():
    graph = build_graph()

    state = {
        "input": {
            "category": "AI",
            "geography": "India",
            "audience_size": 3000
        },
        "outputs": {},
        "agent_meta": {},
        "shared_memory": {},
        "logs": [],
        "errors": []
    }

    logger.info("Starting EventForge pipeline...")
    result = await graph.ainvoke(state)
    logger.info("Graph execution completed")

    logger.debug(f"Final state: {result}")
    
    if "sponsor_agent" in result["outputs"]:
        logger.info("Sponsor agent output generated successfully")
        logger.debug(result["outputs"]["sponsor_agent"])
    else:
        logger.error("Sponsor agent output missing")
        logger.error(f"Errors: {result['errors']}")
        
    print(result["outputs"]["sponsor_agent"])
    print(result["outputs"]["sponsor_agent"])

if __name__ == "__main__":
    asyncio.run(main())