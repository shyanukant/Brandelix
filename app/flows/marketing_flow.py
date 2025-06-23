# app/flows/marketing_flow.py

# from google.adk.agents import SequentialAgent
# from app.agents.copywriter import CopywriterAgent
# from app.agents.editor import EditorAgent
# from app.agents.designer import ImageAgent

# MarketingFlowAgent = SequentialAgent(
#     name="MarketingFlowAgent",
#     sub_agents=[CopywriterAgent, EditorAgent, ImageAgent]
# )


# app/flows/marketing_flow.py
from google.adk.agents import SequentialAgent
from app.agents.copywriter import CopywriterAgent
from app.agents.editor import EditorAgent

MarketingFlowAgent = SequentialAgent(
    name="MarketingFlowAgent",
    sub_agents=[CopywriterAgent, EditorAgent]
)
