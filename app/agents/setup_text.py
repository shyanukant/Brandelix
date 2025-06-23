# app/setup_text.py

from google import genai
import os

client_text = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    vertexai=False  # ensures API key path
)
