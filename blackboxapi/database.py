from abc import ABC, abstractmethod
from typing import Dict, Optional
from .models import Chat

class DatabaseInterface(ABC):
    @abstractmethod
    def get_or_create_chat(self, chat_id: str) -> Chat:
        pass

    @abstractmethod
    def save_chat(self, chat: Chat) -> None:
        pass

    @abstractmethod
    def delete_chat(self, chat_id: str) -> None:
        pass

    @abstractmethod
    def get_chat(self, chat_id: str) -> Optional[Chat]:
        pass

class DictDatabase(DatabaseInterface):
    def __init__(self):
        self.chats: Dict[str, Chat] = {}

    def get_or_create_chat(self, chat_id: str) -> Chat:
        return self.chats.setdefault(chat_id, Chat(self, chat_id))

    def save_chat(self, chat: Chat) -> None:
        self.chats[chat.chat_id] = chat

    def delete_chat(self, chat_id: str) -> None:
        self.chats.pop(chat_id, None)

    def get_chat(self, chat_id: str) -> Optional[Chat]:
        return self.chats.get(chat_id)
