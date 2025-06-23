# app/agents/agents_schemas.py
from pydantic import BaseModel

class EditRequest(BaseModel):
    base_post: str
    edit_instruction: str
