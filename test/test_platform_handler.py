# test_platform_handler.py

from app.agents.platform_handler import PlatformHandler
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import asyncio

async def test_platform_handler():
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="postpilot",
        user_id="shyanu",
        session_id="demo_platform",
        state={
            "edited_post": "Here's my polished blog teaser. Check it out!",
            "post_time": "2025-06-23T10:00:00Z",
            "current_platform": "twitter"
        }
    )

    runner = Runner(agent=PlatformHandler, app_name="postpilot", session_service=session_service)
    user_input = types.Content(role='user', parts=[types.Part(text="Adapt and schedule post")])

    async for event in runner.run_async(user_id="shyanu", session_id="demo_platform", new_message=user_input):
        if event.is_final_response():
            print("\n✅ Adapted Text:", event.session.state.get("platform_twitter"))
            print("✅ Schedule:", event.session.state.get("scheduled_twitter"))

asyncio.run(test_platform_handler())
