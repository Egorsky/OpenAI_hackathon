import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    
    return app

app = create_app()

