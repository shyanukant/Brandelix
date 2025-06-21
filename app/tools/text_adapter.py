from google.adk.tools import FunctionTool

def adapt_text(tool_context):
    platform = tool_context.state.get("current_platform")
    text = tool_context.state.get("edited_post", "")
    
    if not platform or not text:
        return {"error": "Missing platform or text"}

    if platform == "twitter":
        adapted = text[:260] + " #ShortPost"
    elif platform == "instagram":
        adapted = text + "\n\n✨ Follow @postpilot for more!"
    else:
        adapted = text + "\n\n🚀 Like, share, and comment!"

    key = f"platform_{platform}"
    tool_context.state[key] = adapted

    return {"platform": platform, "text": adapted}

PlatformTextAdapterTool = FunctionTool(adapt_text)
