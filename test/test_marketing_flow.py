# test_marketing_flow.py

from app.flows.marketing_flow import MarketingFlowAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import asyncio

async def test_full_marketing_flow():
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="BrandElix",
        user_id="shyanu",
        session_id="demo_full",
        state={
            "goal": "Promote my new blog on productivity hacks",
            "tone": "funny",
            "platforms": ["twitter", "instagram"],
            "post_time": "2025-06-24T10:30:00Z"
        }
    )

    runner = Runner(agent=MarketingFlowAgent, app_name="BrandElix", session_service=session_service)

    user_input = types.Content(role='user', parts=[types.Part(text="Start marketing flow")])

    async for event in runner.run_async(user_id="shyanu", session_id="demo_full", new_message=user_input):
        if event.is_final_response():
            print("\n✅ Flow complete.\n")

            print("🧠 Base Post:", event.session.state.get("base_post"))
            print("🧼 Edited Post:", event.session.state.get("edited_post"))
            print("🎨 Design Prompt:", event.session.state.get("image_prompt"))

            for platform in ["twitter", "instagram"]:
                print(f"\n📱 {platform.capitalize()} Adapted:", event.session.state.get(f"platform_{platform}"))
                print(f"⏰ Scheduled: ", event.session.state.get(f"scheduled_{platform}"))

asyncio.run(test_full_marketing_flow())
# This code tests the full marketing flow by simulating a session where a user wants to promote a blog post across multiple platforms.