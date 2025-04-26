import os
import time
from typing import Dict, List, Optional, Any
import uuid
import dotenv

from zep_cloud.client import AsyncZep
from zep_cloud.types import Message as ZepMessage
from zep_cloud import NotFoundError

dotenv.load_dotenv()
ZEP_API_KEY = os.environ.get("ZEP_API_KEY")

class AsyncZepMemoryManager:
    """
    A class to manage memory using AsyncZep for the OpenAI Agents SDK.
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
        Initialize the AsyncZepMemoryManager.

        Args:
            session_id: Optional session ID. If not provided, a new one will be generated.
            user_id: Optional user ID. If not provided, a new one will be generated.
            email: Optional email address for the user.
            first_name: Optional first name for the user.
            last_name: Optional last name for the user.
        """
        self.session_id = session_id or str(uuid.uuid4())
        self.user_id = user_id or f"user-{str(uuid.uuid4())[:8]}"
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.ignore_assistant = ignore_assistant
        self.zep_client: AsyncZep | None = None

    async def initialize(self):
        """
        Initialize the AsyncZep client, create or get the user, and create a new memory session.
        """
        if not ZEP_API_KEY:
            print(
                "Error: ZEP_API_KEY environment variable not set. Cannot initialize AsyncZep client."
            )
            return

        self.zep_client = AsyncZep(api_key=ZEP_API_KEY)

        # Create or get the user
        try:
            # Try to get the user first
            await self.zep_client.user.get(self.user_id)
            print(f"Using existing user: {self.user_id}")

        except NotFoundError:
            await self.zep_client.user.add(
                user_id=self.user_id,
                first_name=self.first_name,
                last_name=self.last_name,
                email=self.email,
            )
            print(f"Created new user with ID: {self.user_id}")

        # Generate a timestamp-based session ID for a new session each time
        timestamp = int(time.time())
        self.session_id = f"{self.session_id}-{timestamp}"
        print(f"Creating new session with ID: {self.session_id}")

        # Always create a new memory session with the user ID
        await self.zep_client.memory.add_session(
            session_id=self.session_id,
            user_id=self.user_id,
        )

    async def add_message(self, message: dict) -> None:
        """
        Add a message to Zep memory.

        Args:
            message: The message to add to memory.
        """
        # Convert OpenAI message to Zep message
        role = message.get("role", None)

        zep_message_role = ""
        if role == "user" and self.first_name:
            zep_message_role = self.first_name
            if self.last_name:
                zep_message_role += " " + self.last_name

        zep_message = ZepMessage(
            role=zep_message_role
            if zep_message_role
            else "assistant",  # role in Zep is the name of the user
            role_type=role,  # Use the role directly
            content=message.get("content", ""),
        )

        # Add message to Zep memory using AsyncZep client
        if not self.zep_client:
            raise ValueError("Zep client not initialized")

        await self.zep_client.memory.add(
            session_id=self.session_id,
            messages=[zep_message],
            ignore_roles=["assistant"] if self.ignore_assistant else None,
        )

    async def get_memory(self) -> str:
        """
        Get the memory context string from Zep memory instead of creating a summary.

        Returns:
            A string containing the memory context from Zep.
        """
        try:
            if not self.zep_client:
                raise ValueError("Zep client not initialized")

            # Use memory.get to retrieve memory context for the session
            memory = await self.zep_client.memory.get(session_id=self.session_id)

            # Use the context string provided by Zep instead of creating a summary
            if memory.context:
                return memory.context

            return "No conversation history yet."
        except NotFoundError:
            print("Session not found.")
            raise
        except Exception as e:
            print(f"Error getting memory context: {e}")
            raise

    async def search_memory(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search Zep memory for relevant facts based on a query.
        Node search is also supported by Zep but not implemented here.

        Args:
            query: The query to search for relevant facts.
            limit: Maximum number of facts to return.

        Returns:
            A list of relevant facts.
        """

        formatted_messages = []
        # First try to use graph.search to find relevant information
        try:
            # Check if zep_client is initialized
            if not self.zep_client:
                raise ValueError("Zep client not initialized")

            # Use the user_id property directly instead of getting it from the session
            if self.user_id:
                # Use graph.search to find relevant edges. Facts reside on graph edges
                search_response = await self.zep_client.graph.search(
                    query=query, user_id=self.user_id, scope="edges", limit=limit
                )

                if search_response and search_response.edges:
                    # Convert graph search results to the expected format
                    formatted_messages = [
                        {
                            "role": "assistant",  # These are facts, so mark them as from the assistant
                            "content": edge.fact,
                        }
                        for edge in search_response.edges[:limit]
                    ]
                    print(
                        f"Memory search found {len(formatted_messages)} relevant facts from graph search"
                    )
                    return formatted_messages
        except NotFoundError:
            print("User not found.")
            raise
        except Exception as search_error:
            print(f"Graph search error: {search_error}")
            raise

        return formatted_messages
