import asyncio

from eventforge.graph.builder import build_graph
from eventforge.utils.logging import get_logger, setup_logging

setup_logging()
logger = get_logger(__name__)


def _safe_int_input(prompt: str, optional: bool = False):
    val = input(prompt).strip()

    if optional and val == "":
        return None

    try:
        return int(val)
    except ValueError:
        print("Invalid number. Try again.")
        return _safe_int_input(prompt, optional)


async def main():
    graph = build_graph()

    category = input("Enter conference category: ")
    geography = input("Enter geography: ")
    audience_size = _safe_int_input("Enter audience size: ")

    budget_usd = _safe_int_input(
        "Enter budget in USD (optional, press Enter to skip): ", optional=True
    )

    duration_days = _safe_int_input(
        "Enter duration in days (default = 1): ", optional=True
    )

    state = {
        "input": {
            "category": category,
            "geography": geography,
            "audience_size": audience_size,
            "budget_usd": budget_usd,
            "duration_days": duration_days,
        },
        "outputs": {},
        "agent_meta": {},
        "shared_memory": {},
        "logs": [],
        "errors": [],
    }

    logger.info("Starting EventForge pipeline...")

    result = await graph.ainvoke(state)

    logger.info("Graph execution completed")

    print("\n=== FINAL OUTPUT ===\n")
    print(result["outputs"]["final_agent"])


if __name__ == "__main__":
    asyncio.run(main())
