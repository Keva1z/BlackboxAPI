from dataclasses import dataclass
from collections import deque
import uuid
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class Message:
    """Represents a message in the chat conversation.
    
    Attributes:
        content (str): The actual content of the message
        role (str): The role of the message sender (user/assistant)
        id (str): Unique identifier for the message
        timestamp (str): ISO format timestamp of message creation
    """
    content: str
    role: str
    id: str = None
    timestamp: str = None
    image: Optional[str] = None

    def __post_init__(self):
        """Initialize optional fields after dataclass creation."""
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert the message to a dictionary representation.
        
        Returns:
            Dict[str, Any]: Dictionary containing message data
        """
        if self.image:
            return {
                "id": self.id,
                "content": self.content,
                "role": self.role,
                "data": {
                    "fileText": "",
                    "imageBase64": self.image,
                    "title": None,
                }
            }
        
        return {
            "id": self.id,
            "content": self.content,
            "role": self.role,
        }

@dataclass
class AgentMode:
    """Represents an AI agent mode with specific capabilities.
    
    Attributes:
        mode (bool): Whether the agent mode is enabled
        id (str): Unique identifier for the agent mode
        name (str): Human-readable name of the agent mode
        description (str): Optional description of the agent's capabilities
    """
    mode: bool
    id: str
    name: str
    description: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert the agent mode to a dictionary representation.
        
        Returns:
            Dict[str, Any]: Dictionary containing agent mode data
        """
        data = {
            "mode": self.mode,
            "id": self.id,
            "name": self.name
        }
        if self.description:
            data["description"] = self.description
        return data

@dataclass
class Model:
    """Represents an AI language model.
    
    Attributes:
        name (str): Human-readable name of the model
        id (str): Unique identifier for the model
        max_tokens (int): Maximum tokens the model can process
        supports_streaming (bool): Whether the model supports streaming responses
    """
    name: str
    id: str
    max_tokens: int = 4096
    supports_streaming: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert the model to a dictionary representation.
        
        Returns:
            Dict[str, Any]: Dictionary containing model data
        """
        return {
            "name": self.name,
            "id": self.id,
            "max_tokens": self.max_tokens,
            "supports_streaming": self.supports_streaming
        }

class Chat:
    """Represents a chat session with message history.
    
    This class manages a conversation between a user and an AI assistant,
    maintaining a limited history of messages and handling persistence.
    
    Attributes:
        MAX_MESSAGES (int): Maximum number of messages to keep in history
        database: Database interface for persistence
        messages (deque): Double-ended queue of messages
        chat_id (str): Unique identifier for the chat
        created_at (str): ISO format timestamp of chat creation
        metadata (Dict): Additional chat metadata
    """
    MAX_MESSAGES = 25

    def __init__(self, database, chat_id: str = None):
        """Initialize a new chat session.
        
        Args:
            database: Database interface for persistence
            chat_id (str, optional): Unique identifier for the chat
        """
        self.database = database
        self.messages: deque = deque(maxlen=self.MAX_MESSAGES)
        self.chat_id: str = chat_id or str(uuid.uuid4())
        self.created_at: str = datetime.utcnow().isoformat()
        self.metadata: Dict[str, Any] = {
            "message_count": 0,
            "last_updated": self.created_at
        }
        logger.debug(f"Created new chat session with ID: {self.chat_id}")

    def add_message(self, content: str, role: str, image: Optional[str] = None) -> Message:
        """Add a new message to the chat history.
        
        Args:
            content (str): The message content
            role (str): The role of the message sender
            
        Returns:
            Message: The created message object
            
        Raises:
            ValueError: If content is empty or role is invalid
        """
        if not content.strip():
            raise ValueError("Message content cannot be empty")
        if role not in ["user", "assistant"]:
            raise ValueError("Invalid message role")

        message = Message(content=content, role=role, id=str(uuid.uuid4()), image=image)
        self.messages.append(message)
        self.metadata.update({
            "message_count": len(self.messages),
            "last_updated": datetime.utcnow().isoformat()
        })
        
        if self.database:
            self.database.save_chat(self)
            
        logger.debug(f"Added {role} message to chat {self.chat_id}")
        return message

    def get_messages(self) -> List[Message]:
        """Get all messages in the chat history.
        
        Returns:
            List[Message]: List of all messages in chronological order
        """
        return list(self.messages)

    def clear_history(self) -> None:
        """Clear all messages from the chat history."""
        self.messages.clear()
        self.metadata["message_count"] = 0
        self.metadata["last_updated"] = datetime.utcnow().isoformat()
        logger.info(f"Cleared history for chat {self.chat_id}")

# Define available models with their capabilities
GPT4 = Model(
    name="GPT-4",
    id="gpt-4o",
    max_tokens=8192,
    supports_streaming=False
)

CLAUDE = Model(
    name="Claude",
    id="claude-sonnet-3.5",
    max_tokens=8192,
    supports_streaming=False
)

GEMINI = Model(
    name="Gemini",
    id="gemini-pro",
    max_tokens=4096,
    supports_streaming=False
)

BLACKBOX = Model(
    name="Blackbox AI",
    id="blackbox-ai",
    max_tokens=2048,
    supports_streaming=False
)
