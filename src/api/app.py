import os
from typing import Dict

from fastapi import FastAPI
from dotenv import load_dotenv
from opik.integrations.openai.agents import OpikTracingProcessor
from agents import set_trace_processors, set_default_openai_key

from .session_store import agents as _agents
from ..utils  import load_yaml
from .routes import router as chat_router
from contextlib import asynccontextmanager

load_dotenv()
set_default_openai_key(os.environ["OPENAI_API_KEY"])
config = load_yaml("config.yaml")

app = FastAPI(
    title="Crypto Assistant API",
    version="0.1.0",
    description="An LLM-backed API with memory and tools",
)

# Tracing is performed by using Opik
@asynccontextmanager
async def lifespan(app: FastAPI):
    set_trace_processors(processors=[OpikTracingProcessor()])
    yield

app.include_router(chat_router)