# test_copywriter_run.py

from app.agents.copywriter import CopywriterAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

import asyncio
from dotenv import load_dotenv
load_dotenv()

async def test_copywriter():
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="BrandElix",
        user_id="shyanu",
        session_id="demo01",
        state={"goal": "Promote my new blog post about remote work", "tone": "funny"},
        
    )

    runner = Runner(agent=CopywriterAgent, app_name="BrandElix", session_service=session_service)
    user_input = types.Content(role='user', parts=[types.Part(text="Create a post!")])

    async for event in runner.run_async(user_id="shyanu", session_id="demo01", new_message=user_input):
        if event.is_final_response():
            print("\n✅ Final Output:\n", event.content.parts[0].text)

asyncio.run(test_copywriter())
