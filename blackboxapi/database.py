from abc import ABC, abstractmethod
from typing import Dict, Optional, List, Any
from .models import Chat, Message
from .exceptions import DatabaseError
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DatabaseInterface(ABC):
    """Abstract base class defining the interface for chat storage implementations.
    
    This interface provides the basic operations needed to store and retrieve chat data.
    Implementations should handle persistence, caching, and error recovery as needed.
    """
    
    @abstractmethod
    def get_or_create_chat(self, chat_id: str) -> Chat:
        """Retrieve an existing chat or create a new one if it doesn't exist.
        
        Args:
            chat_id (str): Unique identifier for the chat.
            
        Returns:
            Chat: The retrieved or newly created chat object.
            
        Raises:
            DatabaseError: If there's an error accessing the storage.
        """
        pass

    @abstractmethod
    def save_chat(self, chat: Chat) -> None:
        """Save a chat object to storage.
        
        Args:
            chat (Chat): The chat object to save.
            
        Raises:
            DatabaseError: If there's an error saving to storage.
        """
        pass

    @abstractmethod
    def delete_chat(self, chat_id: str) -> None:
        """Delete a chat from storage.
        
        Args:
            chat_id (str): Unique identifier of the chat to delete.
            
        Raises:
            DatabaseError: If there's an error deleting from storage.
        """
        pass

    @abstractmethod
    def get_chat(self, chat_id: str) -> Optional[Chat]:
        """Retrieve a chat from storage.
        
        Args:
            chat_id (str): Unique identifier of the chat to retrieve.
            
        Returns:
            Optional[Chat]: The chat object if found, None otherwise.
            
        Raises:
            DatabaseError: If there's an error accessing storage.
        """
        pass

    @abstractmethod
    def list_chats(self) -> List[str]:
        """List all available chat IDs.
        
        Returns:
            List[str]: List of chat IDs in storage.
            
        Raises:
            DatabaseError: If there's an error accessing storage.
        """
        pass

class DictDatabase(DatabaseInterface):
    """In-memory implementation of DatabaseInterface using a dictionary.
    
    This implementation stores all data in memory and is suitable for testing
    and development purposes. Data is lost when the application restarts.
    
    Attributes:
        chats (Dict[str, Chat]): Dictionary storing chat objects.
        metadata (Dict[str, Dict]): Dictionary storing chat metadata.
    """

    def __init__(self):
        """Initialize an empty in-memory database."""
        self.chats: Dict[str, Chat] = {}
        self.metadata: Dict[str, Dict[str, Any]] = {}
        logger.info("Initialized in-memory database")

    def get_or_create_chat(self, chat_id: str) -> Chat:
        """Implementation of get_or_create_chat."""
        try:
            if chat_id not in self.chats:
                logger.debug(f"Creating new chat with ID: {chat_id}")
                self.chats[chat_id] = Chat(self, chat_id)
                self.metadata[chat_id] = {
                    'created_at': datetime.utcnow().isoformat(),
                    'message_count': 0,
                    'last_updated': datetime.utcnow().isoformat()
                }
            return self.chats[chat_id]
        except Exception as e:
            logger.error(f"Error in get_or_create_chat: {str(e)}")
            raise DatabaseError(f"Failed to get or create chat: {str(e)}")

    def save_chat(self, chat: Chat) -> None:
        """Implementation of save_chat."""
        try:
            if not isinstance(chat, Chat):
                raise ValueError("Invalid chat object")
                
            self.chats[chat.chat_id] = chat
            self.metadata[chat.chat_id].update({
                'message_count': len(chat.get_messages()),
                'last_updated': datetime.utcnow().isoformat()
            })
            logger.debug(f"Saved chat {chat.chat_id} with {len(chat.get_messages())} messages")
        except Exception as e:
            logger.error(f"Error in save_chat: {str(e)}")
            raise DatabaseError(f"Failed to save chat: {str(e)}")

    def delete_chat(self, chat_id: str) -> None:
        """Implementation of delete_chat."""
        try:
            self.chats.pop(chat_id, None)
            self.metadata.pop(chat_id, None)
            logger.info(f"Deleted chat {chat_id}")
        except Exception as e:
            logger.error(f"Error in delete_chat: {str(e)}")
            raise DatabaseError(f"Failed to delete chat: {str(e)}")

    def get_chat(self, chat_id: str) -> Optional[Chat]:
        """Implementation of get_chat."""
        try:
            chat = self.chats.get(chat_id)
            if chat:
                logger.debug(f"Retrieved chat {chat_id}")
            else:
                logger.debug(f"Chat {chat_id} not found")
            return chat
        except Exception as e:
            logger.error(f"Error in get_chat: {str(e)}")
            raise DatabaseError(f"Failed to get chat: {str(e)}")

    def list_chats(self) -> List[str]:
        """Implementation of list_chats."""
        try:
            return list(self.chats.keys())
        except Exception as e:
            logger.error(f"Error in list_chats: {str(e)}")
            raise DatabaseError(f"Failed to list chats: {str(e)}")

    def get_chat_metadata(self, chat_id: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a specific chat.
        
        Args:
            chat_id (str): The ID of the chat.
            
        Returns:
            Optional[Dict[str, Any]]: Chat metadata if found, None otherwise.
        """
        return self.metadata.get(chat_id)

    def clear_all(self) -> None:
        """Clear all chats and metadata from storage.
        
        This is useful for testing or when a complete reset is needed.
        """
        self.chats.clear()
        self.metadata.clear()
        logger.warning("Cleared all chats and metadata from storage")
