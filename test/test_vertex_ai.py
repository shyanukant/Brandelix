import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from google.oauth2 import service_account
import os

# Load credentials (ensure GOOGLE_APPLICATION_CREDENTIALS is set in your .env or environment)
from dotenv import load_dotenv
load_dotenv()
cred = service_account.Credentials.from_service_account_file(
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
)

# Initialize Vertex AI
vertexai.init(project="brandelix", location="us-central1", credentials=cred)

# Load the Imagen‑4 Ultra model
model = ImageGenerationModel.from_pretrained(
    "imagen-4.0-ultra-generate-preview-06-06"
)

# Generate a single square image
images = model.generate_images(
    prompt="A banner to promote my new blog post about remote work, professional yet fun",
    number_of_images=1,
    aspect_ratio="1:1",
    language="en",
    safety_filter_level="block_medium_and_above",  # moderate safety filtering
    person_generation="allow_adult"
)

# Save output
output_path = "remote_work_banner.png"
images[0].save(location=output_path, include_generation_parameters=False)

print(f"Image generated and saved as {output_path}")
