from app.agents.designer import DesignerAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import asyncio

from dotenv import load_dotenv
load_dotenv()

async def test_designer_image():
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="BrandElix",
        user_id="shyanu",
        session_id="demo_img_test",
        state={
            "base_post": "Check out my new WFH productivity blog!",
            "tone": "funny"
        }
    )

    runner = Runner(agent=DesignerAgent, app_name="BrandElix", session_service=session_service)

    print("Edited Post:", session.state["base_post"] )
    user_input = types.Content(role="user", parts=[types.Part(text="Generate visual" + session.state["base_post"])])
    async for event in runner.run_async(
    user_id="shyanu",
    session_id="demo_img_test",
    new_message=user_input
):
        if event.is_final_response():
            # print("✅ Done. Image:", event.session.state.get("image_path"))
            print("✅ Done. Image:", event)

asyncio.run(test_designer_image())
