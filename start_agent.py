import asyncio
from dotenv import load_dotenv
load_dotenv() # Load variables from .env
from app.services.agent_brain import AutonomousAgent

async def main():
    agent = AutonomousAgent()
    print("🚀 FinSight Autonomous Agent Initializing...")
    await agent.start_monitoring()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nAgent stopped by user.")
