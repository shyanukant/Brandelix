from google.adk.agents import LlmAgent
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
