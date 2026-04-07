import asyncio
import json
from backend.orchestrator import run_conference_planner

async def main() -> None:
    """
    Entry point for running the system.
    Hardcoded test input for now.
    Later: becomes FastAPI endpoint or Streamlit call.

    Prints final ConferencePlan as formatted JSON.
    """
    ...

if __name__ == "__main__":
    asyncio.run(main())