import asyncio
from agents import Agent, Runner, set_trace_processors, set_default_openai_key
from tools import fetch_aave_info, check_scam_address, get_search_memory_tool, web_search_preview
from .memory import AsyncZepMemoryManager
from .utils import load_yaml
from opik.integrations.openai.agents import OpikTracingProcessor
from dotenv import load_dotenv
from typing import Optional
import time 
import os 

load_dotenv()
set_default_openai_key(os.environ.get("OPENAI_API_KEY"))
config = load_yaml("config.yaml")

class AsyncZepMemoryAgent:
    """
    An agent that uses AsyncZep for memory with OpenAI Agents SDK.
    """

    def __init__(
        self,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        ignore_assistant: bool = False,
    ):
        """
        Initialize the AsyncZepMemoryAgent.

        Args:
            session_id: Optional session ID. If not provided, a new one will be generated.
            user_id: Optional user ID. If not provided, a new one will be generated.
            email: Optional email address for the user.
            first_name: Optional first name for the user.
            last_name: Optional last name for the user.
            ignore_assistant: Optional flag to indicate whether to persist the assistant's response to the user graph.
        """
        self.memory_manager = AsyncZepMemoryManager(
            session_id, user_id, email, first_name, last_name, ignore_assistant
        )
        self.agent = None

    async def initialize(self):
        """
        Initialize the AsyncZep memory manager and create OpenAI agent with tools.
        """
        # Initialize the AsyncZep memory manager
        await self.memory_manager.initialize()

        search_memory = get_search_memory_tool(self.memory_manager)

        # Get memory context to include in the system message
        memory_context = await self.memory_manager.get_memory()

        # Create the agent with memory tools and context-enhanced system message
        self.agent = Agent(
            name="Orchestrator Agent wth Memory",
            model=config["orchestrator_agent"]["model"],
            instructions=(config["orchestrator_agent"]["instructions"] + "\n" + f"Memory Context: {memory_context}"),
            tools=[
                fetch_aave_info,
                check_scam_address,
                search_memory,
                web_search_preview,
            ]
        )

    async def chat(self, user_input: str, medieval_mode) -> str:
        """
        Chat with the agent and store the conversation in Zep memory.

        Args:
            user_input: The user's input message.

        Returns:
            The agent's response.
        """
        # Check if agent and memory manager are initialized
        if not self.agent:
            return "Error: Agent not initialized. Please check your OpenAI API key."

        if not self.memory_manager.zep_client:
            return "Error: AsyncZep client not initialized. Please set the ZEP_API_KEY environment variable."

        # Store the user message in Zep memory
        await self.memory_manager.add_message({"role": "user", "content": user_input})

        # Update the agent's instructions with the latest memory context
        memory_context = await self.memory_manager.get_memory()
        if medieval_mode:
            self.agent.instructions = (
                config["orchestrator_agent"]["medieval_instructions"] + "\n" + f"Memory Context: {memory_context}"
            )
        else:
            self.agent.instructions = (
                config["orchestrator_agent"]["instructions"] + "\n" + f"Memory Context: {memory_context}"
            )
        # Run the agent with the user input directly
        result = await Runner.run(self.agent, user_input)

        # Extract the agent's response
        agent_response = result.final_output

        # Store the agent's response in Zep memory
        await self.memory_manager.add_message(
            {"role": "assistant", "content": agent_response}
        )

        return agent_response


async def run_agent(
    session_id: Optional[str] = None,
    user_id: Optional[str] = None,
    email: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    ignore_assistant: bool = False,
):
    """
    Run the AsyncZepMemoryAgent in interactive mode for continuous conversation.

    Args:
        session_id: Optional session ID. If not provided, a new one will be generated.
        user_id: Optional user ID. If not provided, a new one will be generated.
        email: Optional email address for the user.
        first_name: Optional first name for the user.
        last_name: Optional last name for the user.
        ignore_assistant: Optional flag to indicate whether to persist the assistant's response to the user graph.
    """
    print(
        "\nInitializing AsyncZep Memory Agent with OpenAI Agents SDK (Interactive Mode)..."
    )

    # Create a memory agent with the provided parameters
    if not session_id:
        session_id = f"interactive-session-{int(time.time())}"

    memory_agent = AsyncZepMemoryAgent(
        session_id, user_id, email, first_name, last_name, ignore_assistant
    )

    # Initialize the agent
    await memory_agent.initialize()

    print("\n=== Agent Factor ===")
    print("Type 'exit', 'quit', or 'bye' to end the conversation.")
    print("Type 'memory' to see the current memory context.")
    print("=== Start Conversation ===\n")

    while True:
        # Get user input
        user_input = input("You: ")

        # Check for exit commands
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("\nExiting interactive mode. Goodbye!")
            break

        # Check for memory command
        if user_input.lower() == "memory":
            memory_context = await memory_agent.memory_manager.get_memory()
            print(f"\n=== Memory Context ===\n{memory_context}\n")
            continue

        # Process the user input and get the agent's response
        agent_response = await memory_agent.chat(user_input)
        print(f"Agent: {agent_response}\n")
    

async def main():
    # Dummy data that we used for testing purposes
    session_id = f"demo-session-{int(time.time())}"
    user_id     = "123"
    email       = "abc@gmail.com"
    first_name  = "John"
    last_name   = "Doe"
    ignore_assistant = False

    await run_agent(
        session_id,
        user_id,
        email,
        first_name,
        last_name,
        ignore_assistant=ignore_assistant,
    )
    
if __name__ == "__main__":
    set_trace_processors(processors=[OpikTracingProcessor()])
    asyncio.run(main())