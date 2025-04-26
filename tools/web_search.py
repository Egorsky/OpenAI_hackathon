from openai import OpenAI
import os
from dotenv import load_dotenv
from agents import function_tool
from pydantic import BaseModel
from src.utils import load_yaml
from typing import Dict

class UserInput(BaseModel):
    query: str

load_dotenv()

config = load_yaml("config.yaml")

client = OpenAI()

@function_tool
def web_search_preview(text: UserInput) -> Dict[str, str]:
    """
    Perform a web search using OpenAI's web_search_preview tool.
    """
    response = client.responses.create(
        model=os.environ.get("WEB_SEARCH_MODEL"),
        tools=[{
            "type": "web_search_preview",
            "search_context_size": "medium",
        }],
        input=text
    )
    return {"Answer" : response.output_text}
