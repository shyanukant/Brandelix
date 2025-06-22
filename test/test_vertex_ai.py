
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from google.oauth2 import service_account
import os
from dotenv import load_dotenv
load_dotenv()

cred = service_account.Credentials.from_service_account_file(
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "path/to/your/service-account.json")
)
# TODO(developer): Update and un-comment below lines
# PROJECT_ID = "your-project-id"
output_file = "input-image.png"
# prompt = "" # The text prompt describing what you want to see.

vertexai.init(project="brandelix", location="us-central1", credentials=cred)

model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")

images = model.generate_images(
    prompt="Promote my new blog post about remote work",
    # Optional parameters
    number_of_images=1,
    language="en",
    # You can't use a seed value and watermark at the same time.
    # add_watermark=False,
    # seed=100,
    aspect_ratio="1:1",
    safety_filter_level="block_some",
    person_generation="allow_adult",
)

images[0].save(location=output_file, include_generation_parameters=False)

# Optional. View the generated image in a notebook.
# images[0].show()

print(f"Created output image using {len(images[0]._image_bytes)} bytes")
# Example response:
# Created output image using 1234567 bytes