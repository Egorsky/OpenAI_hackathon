import os
import time
from functools import wraps
from fastapi import FastAPI
from src.agent import AsyncZepMemoryAgent
from fastapi.middleware.cors import CORSMiddleware

memory_agent = AsyncZepMemoryAgent(
    session_id=f"web-session-{int(time.time())}",
    user_id="web_user",
    email="web@example.com"
    first_name="Web",
    last_name="User",
)

def llm_response(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            if memory_agent.agent is None:
                await memory_agent.initialize()
            
            # Get the user message from the payload    
            user_message = kwargs.get("payload", {}).get("message", "")
            
            # Get response
            response = await memory_agent.chat(user_message)
            
            return{
                "response": response,
                "status": "success",
                "original_payload": kwargs.get("payload"),
            }
        except Exception as e:
            return {
                "response": str(e),
                "status": "error",
                "original_payload": kwargs.get("payload", {}),
            }
    return wrapper

def create_app() -> FastAPI:
    app = FastAPI(
        title="Agent Factor API",
        description="FastAPI backend with LLM agent.",
        version="1.0.0",
        )
    origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
    
    app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    @app.post("/api/echo")
    async def echo(payload: dict):
        """Return the recieved JSON"""
        return {"received": payload}
    
    @app.post("/api/chat")
    @llm_response
    async def chat(payload: dict):
        """Return the received JSON"""
        return {"response": "LLM resonse should be here",
                "status": "success",
                "original_payload": payload,
                }
    
    return app

app = create_app()

