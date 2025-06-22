"""from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool
from app.agents.image_generator import ImageGeneratorAgent

# Wrap ImageGenerator as a Tool
ImageGenTool = agent_tool.AgentTool(agent=ImageGeneratorAgent(name="ImageGeneratorAgent"))

# DesignerAgent uses this tool to trigger image generation
DesignerAgent = LlmAgent(
    name="DesignerAgent",
    model="gemini-2.0-flash",
    instruction=(
        "Based on the post in 'edited_post' or 'base_post', "
        "create an image_prompt and use the ImageGenTool to generate the image.\n"
        "Only generate the image once using the tool.\n"
        "Do not output a design brief — just generate the image.\n"
    ),
    tools=[ImageGenTool],
    output_key="image"
)
"""
import os
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from google.adk.agents import BaseAgent
from google.adk.events import Event
from google.genai import types
from google.oauth2 import service_account

from dotenv import load_dotenv
load_dotenv()

cred = service_account.Credentials.from_service_account_file(
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "path/to/your/service-account.json")
)
# Initialize Vertex AI once at startup
vertexai.init(
    project=os.getenv("GCP_PROJECT_ID"),
    location=os.getenv("GCP_LOCATION"),
    credentials=cred
)

class DesignerAgent(BaseAgent):
    async def _run_async_impl(self, ctx):
        prompt = ctx.session.state.get("base_post")
        platform = ctx.session.state.get("current_platform", "default")
        if not prompt:
            # yield Event.is_final_response(content="⚠️ No image_prompt found in session state.")
            print("No image_prompt found in session state.")
            return

        # Generate image with Vertex Imagen 3.0
        model = ImageGenerationModel.from_pretrained("imagen-4.0-ultra-generate-preview-06-06")
        response = model.generate_images(prompt=prompt, number_of_images=1, aspect_ratio="1:1")
        img = response[0]

        # Save the image locally
        os.makedirs("generated_images", exist_ok=True)
        filename = f"generated_images/{platform}.png"
        img.save(location=filename)

        ctx.session.state[f"image_path_{platform}"] = filename
        # yield Event.is_final_response(content=f"🖼️ Image saved at `{filename}`.")
        print(Event)

