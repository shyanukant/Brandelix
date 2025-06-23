# pip install google-genai pillow python-dotenv
import os
from google import genai
from google.oauth2 import service_account
from google.genai.types import GenerateContentConfig, Modality
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

def generate_image(prompt: str, project: str, location: str, credentials, output_file: str):
    # Initialize GenAI Client to use Vertex AI with proper credentials
    client = genai.Client(
        vertexai=True,
        project=project,
        location=location,
        credentials=credentials
    )

    # Request both text and image outputs
    config = GenerateContentConfig(
        response_modalities=[Modality.TEXT, Modality.IMAGE]
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=[prompt],
        config=config
    )

    # Iterate through output parts and save image if present
    for part in response.candidates[0].content.parts:
        if part.inline_data and part.inline_data.data:
            image = Image.open(BytesIO(part.inline_data.data))
            image.save(output_file)
            print(f"✅ Image saved to {output_file}")
        elif part.text:
            print("💬 Text output:", part.text)

if __name__ == "__main__":
    sa_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
    if not sa_file or not os.path.exists(sa_file):
        raise RuntimeError("GOOGLE_APPLICATION_CREDENTIALS file is missing or invalid")

    credentials = service_account.Credentials.from_service_account_file(
        sa_file,
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )

    generate_image(
        prompt="A banner to Promote my new blog post about remote work",
        project=os.getenv("GCP_PROJECT_ID", "your-gcp-project-id"),
        location=os.getenv("GCP_LOCATION", "us-central1"),
        credentials=credentials,
        output_file="output.png"
    )
