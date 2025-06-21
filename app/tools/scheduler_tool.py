from google.adk.tools import FunctionTool
from datetime import datetime

def scheduler(tool_context):
    platform = tool_context.state.get("current_platform")
    time = tool_context.state.get("post_time", "NOW")

    key = f"scheduled_{platform}"
    tool_context.state[key] = {
        "platform": platform,
        "time": time,
        "status": "mock_scheduled"
    }

    return {"platform": platform, "status": "scheduled", "time": time}

SchedulerTool = FunctionTool(scheduler)
# SchedulerTool is a tool that simulates scheduling a post for a specific platform.