from pydantic import BaseModel
from typing import Optional, Dict

class CreateSessionRequest(BaseModel):
    user_id:         Optional[str] = None
    email:           Optional[str] = None
    first_name:      Optional[str] = None
    last_name:       Optional[str] = None
    ignore_assistant: bool         = False

class ChatRequest(BaseModel):
    session_id: str
    user_input: str
    medieval_mode: bool = False

class ChatResponse(BaseModel):
    response:         str
    status:           str
    original_payload: Dict