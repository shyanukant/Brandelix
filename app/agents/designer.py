# app/agents/image_agent.py

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from google import genai
import os, base64

client_image = genai.Client(
    vertexai=True,
    project=os.getenv("GCP_PROJECT_ID"),
    location=os.getenv("GCP_LOCATION")
)

def generate_image(prompt: str) -> dict:
    resp = client_image.models.generate_image(
        model="imagen-4.0-ultra-generate-preview-06-06",
        prompt=prompt, number_of_images=1, aspect_ratio="1:1"
    )
    img_bytes = resp.images[0]._image_bytes
    return {"image_b64": base64.b64encode(img_bytes).decode()}

image_tool = FunctionTool(func=generate_image)

ImageAgent = LlmAgent(
    name="ImageAgent",
    model="gemini-2.0-flash",
    tools=[image_tool],
    instruction="Use the `generate_image` tool on the prompt in 'design_prompt' state.",
    output_key="image_b64"
)
