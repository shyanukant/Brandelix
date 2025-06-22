from google.adk.agents import BaseAgent
from google.adk.events import Event
from google.genai import types
from datetime import datetime
import os

class ImageGeneratorAgent(BaseAgent):
    async def _run_async_impl(self, ctx):
        image_bytes = b"\x89PNG\r\n\x1a\n" + b"Mock image bytes for testing."

        filename = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        path = os.path.join("generated_images", filename)
        os.makedirs("generated_images", exist_ok=True)

        with open(path, "wb") as f:
            f.write(image_bytes)

        ctx.session.state["image_path"] = path

        yield Event(
            author=self.name,
            content=types.Content(parts=[
                types.Part.from_bytes(image_bytes),
                types.Part(text=f"✅ Image saved at: {path}")
            ])
        )





#########################################################################
# postpilot_ai/app/agents/designer.py

from google.adk.agents import BaseAgent
from google.genai import types
from google import genai
from google.adk.artifacts import GcsArtifactService

class DesignerAgent(BaseAgent):
    def __init__(self, gcs_bucket: str):
        super().__init__(name="DesignerAgent", description="Generates platform-specific images via Gemini-Imagen")
        # Configure artifact storage
        self.artifact_service = GcsArtifactService(bucket_name=gcs_bucket)

    async def run(self, tool_context):
        # 1️⃣ Get prompt from EditorAgent via state["edited_post"]
        prompt = tool_context.state.get("edited_post")
        platforms = tool_context.state.get("platforms", [])
        client = genai.Client()

        for platform in platforms:
            # Adjust visual style per platform
            plat_prompt = f"{prompt}. Create a high-quality image styled as a {'carousel' if platform=='instagram' else 'banner'} suitable for {platform}."
            response = client.models.generate_content(
                model="gemini-2.0-flash-preview-image-generation",
                contents=plat_prompt,
                config=types.GenerateContentConfig(response_modalities=["IMAGE"])
            )
            img_part = next((p for p in response.candidates[0].content.parts if p.inline_data), None)
            if img_part:
                filename = f"{tool_context.session_id}_{platform}.png"
                version = await tool_context.artifact_service.save_artifact(filename, img_part)
                # Save artifact key and public URL
                tool_context.state[f"image_artifact_{platform}"] = filename
                tool_context.state[f"image_url_{platform}"] = f"gs://{self.artifact_service.bucket_name}/{filename}"
        return tool_context.state
