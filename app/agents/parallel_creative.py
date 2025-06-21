# app/agents/parallel_creative.py

from google.adk.agents import ParallelAgent

# Import sub-agents
from .editor import EditorAgent
from .designer import DesignerAgent

ParallelCreativeAgent = ParallelAgent(
    name="ParallelCreativeAgent",
    sub_agents=[
        EditorAgent,
        DesignerAgent
    ]
)
