# app/agents/image_generator.py

import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from google.oauth2 import service_account
from google.genai import types
import os
from google.adk.tools import FunctionTool, ToolContext
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

# Initialize Vertex AI
vertexai.init(
    project=os.getenv("GCP_PROJECT_ID"),
    location=os.getenv("GCP_LOCATION"),
    credentials=service_account.Credentials.from_service_account_file(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
)
model = ImageGenerationModel.from_pretrained("imagen-4.0-ultra-generate-preview-06-06")

def generate_image(prompt: str, tool_context: ToolContext) -> dict:
    images = model.generate_images(
        prompt=prompt,
        number_of_images=1,
        aspect_ratio="1:1",
        language="en",
        safety_filter_level="block_medium_and_above",
        person_generation="allow_adult",
    )
    data = images[0]._image_bytes
    # Base64 encode binary for JSON safety
    # Wrap bytes in Part
    part = types.Part.from_bytes(data, mime_type="image/png")

    # Save the artifact into ADK session/GCS
    version = tool_context.save_artifact(
        filename="post_image.png",
        artifact=part
    )

    # Store the artifact key or version in session state
    tool_context.state["image_artifact"] = f"post_image.png@{version}"
    # import base64
    # return {"image_b64": base64.b64encode(data).decode("utf-8")}
    # Return a message or metadata
    return {"status": "saved_image", "version": version}

# Wrap it
image_tool = FunctionTool(func=generate_image)
