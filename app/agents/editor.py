# app/agents/editor.py

from google.adk.agents import LlmAgent

EditorAgent = LlmAgent(
    name="EditorAgent",
    model="gemini-2.0-flash",
    instruction=(
        "You are a social media brand editor.\n"
        "Based on the post in session state 'base_post', suggest a design prompt idea "
        "for a visually engaging image.\n\n"
        "Make it platform-agnostic but adaptable to Twitter, Instagram, or Facebook.\n"
        "Be creative — think color, layout, style, and text to overlay.\n"
    ),
    output_key="edited_post"
)
