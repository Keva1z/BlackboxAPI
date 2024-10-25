from dataclasses import dataclass
import uuid
from collections import deque

@dataclass
class Message:
    """Represents a message in the chat."""
    content: str
    role: str
    id: str = None

    def to_dict(self):
        """Convert the message to a dictionary."""
        return {
            "id": self.id,
            "content": self.content,
            "role": self.role
        }

@dataclass
class AgentMode:
    """Represents an agent mode."""
    mode: bool
    id: str
    name: str

    def to_dict(self):
        """Convert the agent mode to a dictionary."""
        return {
            "mode": self.mode,
            "id": self.id,
            "name": self.name
        }

@dataclass
class Model:
    """Represents an AI model."""
    name: str
    id: str

    def to_dict(self):
        """Convert the model to a dictionary."""
        return {
            "name": self.name,
            "id": self.id
        }

class Chat:
    """Represents a chat session."""
    MAX_MESSAGES = 25

    def __init__(self):
        """Initialize a new chat session."""
        self.messages = deque(maxlen=self.MAX_MESSAGES)
        self.chat_id = str(uuid.uuid4())

    def add_message(self, content: str, role: str):
        """Add a new message to the chat."""
        message = Message(content=content, role=role, id=self.chat_id)
        self.messages.append(message)
        return message

    def get_messages(self):
        """Get all messages in the chat."""
        return list(self.messages)

    def clear_history(self):
        """Clear the chat history."""
        self.messages.clear()

# Define available models
GPT4 = Model(name="GPT-4", id="gpt-4o")
CLAUDE = Model(name="Claude", id="claude-3.5-sonnet")
GEMINI = Model(name="Gemini", id="gemini-pro")
BLACKBOX = Model(name="Blackbox AI", id="blackbox-ai")
