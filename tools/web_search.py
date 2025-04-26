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

    if not text:
        raise ValueError("Query must be a non-empty string.")
    
    validation_prompt = (
        f"Analyze if this input related to blockchain topic: '{text}'. "
        "Reply ONLY with 'YES' if it is related, or 'No' if it is not related, "
    )
    validation_response = client.chat.completions.create(
        model=os.environ.get("WEB_SEARCH_MODEL"),
        messages=[{"role": "user", "content": validation_prompt}]
    )

    decision = validation_response.choices[0].message.content.strip().upper()
    if decision == "NO":
        raise ValueError("Blocked query: Input was flagged as not related to blockchain")
    response = client.responses.create(
        model=os.environ.get("WEB_SEARCH_MODEL"),
        tools=[{
            "type": "web_search_preview",
            "search_context_size": "medium",
        }],
        input=text
    )
    return {"Answer" : response.output_text}
