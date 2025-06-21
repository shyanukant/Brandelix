from google.adk.agents import SequentialAgent
from app.tools.text_adapter import PlatformTextAdapterTool
from app.tools.scheduler_tool import SchedulerTool

PlatformHandler = SequentialAgent(
    name="PlatformHandler",
    sub_agents=[
        PlatformTextAdapterTool,
        SchedulerTool
    ]
)
# PlatformHandler is a sequential agent that adapts text for a specific platform and schedules it.