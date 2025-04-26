from fastapi import APIRouter, HTTPException
from .models import CreateSessionRequest, ChatRequest, ChatResponse
from .session_store import agents as _agents 
from ..utils  import load_yaml
from .utils import llm_response
from ..agent import AsyncZepMemoryAgent

config = load_yaml("config.yaml")

router = APIRouter(tags=["chat"])

@router.post("/create-session/{session_id}")
async def create_session(
    session_id: str,
    payload: CreateSessionRequest
):
    if session_id in _agents:
        raise HTTPException(400, f"Session {session_id!r} already exists.")
    
    agent = AsyncZepMemoryAgent(
        session_id=session_id,
        user_id=payload.user_id,
        email=payload.email,
        first_name=payload.first_name,
        last_name=payload.last_name,
        ignore_assistant=payload.ignore_assistant,
    )
    await agent.initialize()
    _agents[session_id] = agent
    return {"message": f"Session {session_id!r} created."}

@router.post("/api/chat", response_model=ChatResponse)
@llm_response
async def chat(payload: ChatRequest):
    agent = _agents.get(payload.session_id)
    if not agent:
        raise HTTPException(404, f"Session {payload.session_id!r} not found.")
    
    reply = await agent.chat(payload.user_input, payload.medieval_mode)
    return {
        "response": reply,
        "status": "success",
        "original_payload": payload.dict(),
    }

@router.get("/memory/{session_id}")
async def read_memory(session_id: str):
    agent = _agents.get(session_id)
    if not agent:
        raise HTTPException(404, f"Session {session_id!r} not found.")
    mem = await agent.memory_manager.get_memory()
    return {"memory": mem}
