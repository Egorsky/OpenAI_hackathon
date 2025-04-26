import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from opik.integrations.openai.agents import OpikTracingProcessor
from agents import set_trace_processors, set_default_openai_key
from .routes import router as chat_router
from contextlib import asynccontextmanager

load_dotenv()
set_default_openai_key(os.environ["OPENAI_API_KEY"])

# Tracing is performed by using Opik
@asynccontextmanager
async def lifespan(app: FastAPI):
    set_trace_processors(processors=[OpikTracingProcessor()])
    yield

app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # permit requests from frontend origin
    allow_credentials=True,  # allow cookies/auth credentials if needed
    allow_methods=["*"],  # allow all HTTP methods (GET, POST, PUT, etc.)
    allow_headers=["*"],  # allow all request headers
)

app.include_router(chat_router)