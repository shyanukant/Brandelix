# test_editor_run.py

from app.agents.editor import EditorAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

import asyncio
from dotenv import load_dotenv
load_dotenv()

async def test_editor():
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="BrandElix",
        user_id="shyanu",
        session_id="demo_editor",
        state={
            "tone": "funny",
            "base_post": "Check my blog post on work from home. It very good and helpfull."
        }
    )

    runner = Runner(agent=EditorAgent, app_name="BrandElix", session_service=session_service)
    user_input = types.Content(role='user', parts=[types.Part(text=f"base_post: {session.state['base_post']}\nTone: {session.state['tone']}")] )

    async for event in runner.run_async(user_id="shyanu", session_id="demo_editor", new_message=user_input):
        if event.is_final_response():
            print("\n✅ Edited Output:\n", event.content.parts[0].text)
            # print("\n✅ Edited Output:\n", event)

asyncio.run(test_editor())
