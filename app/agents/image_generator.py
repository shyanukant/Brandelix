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
