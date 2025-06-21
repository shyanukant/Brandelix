# test_parallel_creative_run.py

from app.agents.parallel_creative import ParallelCreativeAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import asyncio

from dotenv import load_dotenv
load_dotenv()

async def test_parallel_creative():
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="BrandElix",
        user_id="shyanu",
        session_id="demo_parallel",
        state={
            "tone": "funny",
            "base_post": "Check my blog post on remote work. It very helpful and funny!"
        }
    )

    runner = Runner(agent=ParallelCreativeAgent, app_name="BrandElix", session_service=session_service)
    user_input = types.Content(role='user', parts=[types.Part(text="Polish and design this post")] )

    async for event in runner.run_async(user_id="shyanu", session_id="demo_parallel", new_message=user_input):
        if event.is_final_response():
            print("\n🧼 Edited Post:", event.actions.state_delta.get("edited_post"))
            print("\n🎨 Design Prompt:", event.actions.state_delta.get("edited_post"))

asyncio.run(test_parallel_creative())
