from agents import function_tool

def get_search_memory_tool(memory_manager):
    """
    Returns a function‐tool that can search your Zep memory_manager.
    """
    @function_tool
    async def search_memory(query: str) -> str:
        """Search for relevant information facts about the user."""
        results = await memory_manager.search_memory(query)
        if not results:
            return "I couldn't find any relevant facts about the user."

        lines = [f"- {r['role']}: {r['content']}" for r in results]
        formatted = "\n".join(lines)
        return f"Facts about the user:\n{formatted}"

    return search_memory