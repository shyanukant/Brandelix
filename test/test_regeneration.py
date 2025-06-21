# test_regeneration.py

from app.agents.regeneration import RegenerationAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import asyncio

async def test_regenerate_text():
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="postpilot",
        user_id="shyanu",
        session_id="demo_regen_text",
        state={
            "goal": "Promote my new productivity guide",
            "tone": "funny",
            "regenerate_target": "text"
        }
    )

    runner = Runner(agent=RegenerationAgent, app_name="postpilot", session_service=session_service)
    user_input = types.Content(role='user', parts=[types.Part(text="Regenerate please")])

    async for event in runner.run_async(user_id="shyanu", session_id="demo_regen_text", new_message=user_input):
        if event.is_final_response():
            print("\n✅ New base_post:", event.session.state.get("base_post"))

asyncio.run(test_regenerate_text())
