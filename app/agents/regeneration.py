# app/agents/regeneration.py

from google.adk.agents import BaseAgent, LoopAgent
from google.adk.events import Event
from google.genai import types

from app.agents.copywriter import CopywriterAgent
from app.agents.designer import DesignerAgent

# Simple controller to choose which agent to run
class RegenerateSwitchAgent(BaseAgent):
    async def _run_async_impl(self, ctx):
        target = ctx.session.state.get("regenerate_target")

        if not target:
            yield Event(author=self.name, content=types.Content(parts=[
                types.Part(text="⚠️ No regeneration target specified.")
            ]))
            return

        if target == "text":
            async for event in CopywriterAgent.run_async(ctx):
                yield event
        elif target == "image":
            async for event in DesignerAgent.run_async(ctx):
                yield event
        else:
            yield Event(author=self.name, content=types.Content(parts=[
                types.Part(text=f"⚠️ Unknown regeneration target: {target}")
            ]))

# Wrap in LoopAgent for future extensibility
RegenerationAgent = LoopAgent(
    name="RegenerationAgent",
    agent=RegenerateSwitchAgent(name="RegenerateSwitchAgent"),
    max_loops=1  # Set to >1 if you want user to retry again and again
)
