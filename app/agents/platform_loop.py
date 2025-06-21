# app/agents/platform_loop.py

from google.adk.agents import BaseAgent
from google.adk.events import Event
from google.genai import types

# Import the inner handler that processes each platform
from app.agents.platform_handler import PlatformHandler

class LoopOverPlatformsAgent(BaseAgent):
    async def _run_async_impl(self, ctx):
        platforms = ctx.session.state.get("platforms", [])

        if not platforms:
            yield Event(author=self.name, content=types.Content(parts=[
                types.Part(text="⚠️ No platforms specified.")
            ]))
            return

        for platform in platforms:
            ctx.session.state["current_platform"] = platform

            yield Event(author=self.name, content=types.Content(parts=[
                types.Part(text=f"🚀 Processing platform: {platform}")
            ]))

            async for event in PlatformHandler.run_async(ctx):
                yield event

        yield Event(author=self.name, content=types.Content(parts=[
            types.Part(text="✅ Finished scheduling for all platforms.")
        ]))
# This agent loops over each platform specified in the session state
# and invokes the PlatformHandler for each one, allowing for platform-specific processing.



"""
from app.services.artifact import save_image_artifact

class LoopOverPlatformsAgent(BaseAgent):
    async def _run_async_impl(self, ctx):
        platforms = ctx.session.state.get("platforms", [])
        image_prompt = ctx.session.state.get("image_prompt")

        if not platforms:
            yield Event(author=self.name, content=types.Content(parts=[
                types.Part(text="⚠️ No platforms specified.")
            ]))
            return

        for platform in platforms:
            ctx.session.state["current_platform"] = platform

            yield Event(author=self.name, content=types.Content(parts=[
                types.Part(text=f"🚀 Processing platform: {platform}")
            ]))

            # Save mock image for the platform
            if image_prompt:
                save_image_artifact(ctx, platform, image_prompt)

            async for event in PlatformHandler.run_async(ctx):
                yield event

        yield Event(author=self.name, content=types.Content(parts=[
            types.Part(text="✅ Finished scheduling for all platforms.")
        ]))

"""