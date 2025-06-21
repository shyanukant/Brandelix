# app/services/artifact.py

from google.genai import types
import base64

def create_mock_image_from_prompt(prompt: str) -> bytes:
    """
    Returns fake image bytes for testing.
    This can be replaced with real generation logic.
    """
    # This is a fake PNG header (just for mock testing)
    png_header = b"\x89PNG\r\n\x1a\n"
    fake_image_data = prompt.encode("utf-8")[:100]  # use prompt content as part of bytes
    return png_header + fake_image_data

def save_image_artifact(ctx, platform: str, prompt: str):
    fake_bytes = create_mock_image_from_prompt(prompt)
    
    image_part = types.Part.from_bytes(
        fake_bytes,
        mime_type="image/png",
        file_name=f"{platform}_mock.png"
    )
    
    key = f"image_artifact_{platform}"
    ctx.session.state[key] = image_part

    return key
