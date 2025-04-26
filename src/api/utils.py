from functools import wraps
import os

def llm_response(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            # True only if OPENAI_API_KEY is set and nonempty
            has_llm = bool(os.getenv("OPENAI_API_KEY"))

            if not has_llm:
                return {
                    "response": (
                        "I'm currently in demo mode. Please connect an LLM agent "
                        "to enable full functionality. In the meantime, I can show "
                        "you how the interface works!"
                    ),
                    "status": "warning",
                    "original_payload": kwargs.get("payload", {}),
                }

            # Otherwise call your real handler
            return await func(*args, **kwargs)

        except Exception as e:
            return {
                "response": f"Error: {str(e)}",
                "status": "error",
                "original_payload": kwargs.get("payload", {}),
            }

    return wrapper