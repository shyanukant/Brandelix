# runner/main_runner.py
import asyncio, base64
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import GcsArtifactService
from app.flows.marketing_flow import MarketingFlowAgent
from app.agents.image_generator import generate_image
from google.genai import types

artifact_service = GcsArtifactService(bucket_name=os.getenv("GCS_BUCKET"))
async def main():
    ss = InMemorySessionService()
    await ss.create_session(
        app_name="BrandElix", user_id="shyanu", session_id="demo01",
        state={"goal":"Promote remote work blog","tone":"funny"}
    )

    runner = Runner(
        agent=MarketingFlowAgent, 
        app_name="BrandElix", 
        session_service=ss,
        artifact_service=artifact_service
        )
    async for ev in runner.run_async(
        user_id="shyanu", session_id="demo01",
        new_message=types.Content(role="user", parts=[types.Part(text="Start!")])
    ):
        pass  # discard interim events

    # After the initial agent flow:
    session_state = await ss.get_session(
    app_name="BrandElix",
    user_id="shyanu",
    session_id="demo01"
)
    base_post = session_state.state["base_post"]
    design_prompt = session_state.state["edited_post"]

    print("📄 Post:", base_post)
    img_res = generate_image(design_prompt)
    print("🖼️ Image URL:", session_state.state.get("image_url"))
    # with open("final_image.png", "wb") as f:
    #     f.write(img_data)
    # print("🖼️ Image saved → final_image.png")

if __name__ == "__main__":
    asyncio.run(main())
