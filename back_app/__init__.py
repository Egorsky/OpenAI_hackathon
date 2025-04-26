import os
from functools import wraps
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def llm_response(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            # Placeholder for LLM call. Now placeholder.
            has_llm = False
            
            if not has_llm:
                return {
                    "response": "I'm currently in demo mode. Please connect an LLM agent to enable full functionality. In the meantime, I can show you how the interface works!",
                    "status": "warning",
                    "original_payload": kwargs.get("payload", {}),
                }
                
            # Call the actual function when LLM is available
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            return {
                "response": f"Error: {str(e)}",
                "status": "error",
                "original_payload": kwargs.get("payload", {}),
            }
    return wrapper

def create_app() -> FastAPI:
    app = FastAPI(
    
        title="Echo API",
        description="A minimal FastAPI backend that echoes JSON payloads.",
        version="1.0.0",
        )
    origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    
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

