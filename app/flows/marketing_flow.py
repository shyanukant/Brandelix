# app/flows/marketing_flow.py

from google.adk.agents import SequentialAgent

# Import our 3 main building blocks
from app.agents.copywriter import CopywriterAgent
from app.agents.parallel_creative import ParallelCreativeAgent
from app.agents.platform_loop import LoopOverPlatformsAgent

# Root Orchestrator Agent
MarketingFlowAgent = SequentialAgent(
    name="MarketingFlowAgent",
    sub_agents=[
        CopywriterAgent,
        ParallelCreativeAgent,
        LoopOverPlatformsAgent(name="LoopOverPlatformsAgent")
    ]
)
