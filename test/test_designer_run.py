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
            "tone": "funny",
            "image_prompt": "Playful cartoon of a person working from home, coffee cups, slippers, flat 2D style"
        }
    )

    runner = Runner(
        agent=DesignerAgent(name="DesignerAgent"),
        app_name="BrandElix",
        session_service=session_service
    )

    print("⚙️ Starting image generation...")

    user_input = types.Content(role="user", parts=[types.Part(text="Generate visual" + str({session.state['base_post']}))])

    async for event in runner.run_async(
        user_id="shyanu",
        session_id="demo_img_test",
        new_message=user_input
    ):
        if event.is_final_response():
            img_path = event.session.state.get("image_path_default")
            print("✅ Image saved at:", img_path)
            assert img_path and img_path.startswith("generated_images/"), "Image not saved correctly"

asyncio.run(test_designer_image())
