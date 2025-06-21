# test_platform_loop.py

from app.agents.platform_loop import LoopOverPlatformsAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import asyncio

async def test_platform_loop():
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="postpilot",
        user_id="shyanu",
        session_id="demo_loop",
        state={
            "platforms": ["twitter", "instagram"],
            "edited_post": "Want to crush your WFH goals? Here's how.",
            "post_time": "2025-06-23T11:00:00Z"
        }
    )

    runner = Runner(agent=LoopOverPlatformsAgent(name="LoopOverPlatformsAgent"),
                    app_name="postpilot", session_service=session_service)

    user_input = types.Content(role='user', parts=[types.Part(text="Schedule for all platforms")])

    async for event in runner.run_async(user_id="shyanu", session_id="demo_loop", new_message=user_input):
        if event.is_final_response():
            print("\n✅ Finished loop.")
            print("→ Twitter Post:", event.session.state.get("platform_twitter"))
            print("→ Insta Post:", event.session.state.get("platform_instagram"))
            print("→ Schedules:", event.session.state.get("scheduled_twitter"),
                  event.session.state.get("scheduled_instagram"))

asyncio.run(test_platform_loop())
# This code tests the LoopOverPlatformsAgent by simulating a session where a user wants to schedule posts across multiple platforms.
# It initializes the session with a list of platforms, an edited post, and a post time.