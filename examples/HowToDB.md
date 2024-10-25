# 💾 Custom Database Integration

BlackboxAPI provides a flexible interface for integrating various database systems. This guide will help you implement your own database solution.

## 🔧 Implementation Steps

### 1️⃣ Create Database Interface Implementation

Your class must inherit from `DatabaseInterface` and implement all required abstract methods:

```python
from blackboxapi.database import DatabaseInterface
from blackboxapi.models import Chat
from typing import Optional

class YourCustomDatabase(DatabaseInterface):
    def init(self):
        # Initialize your database connection
        pass
        
    def get_or_create_chat(self, chat_id: str) -> Chat:
        # Get existing chat or create new one
        pass
        
    def save_chat(self, chat: Chat) -> None:
        # Save chat to database
        pass

    def delete_chat(self, chat_id: str) -> None:
        # Delete chat from database
        pass

    def get_chat(self, chat_id: str) -> Optional[Chat]:
        # Retrieve chat from database
        pass
```

### 2️⃣ Method Implementation Examples

#### Get or Create Chat

```python
def get_or_create_chat(self, chat_id: str) -> Chat:
    chat = self.get_chat(chat_id)
    if not chat:
        chat = Chat(self, chat_id)
    self.save_chat(chat)
    return chat
```

#### Save Chat

```python
def save_chat(self, chat: Chat) -> None:
    messages_json = json.dumps([m.to_dict() for m in chat.get_messages()])
    
    # Your database-specific save logic here
    
    self.db.save(chat.chat_id, messages_json)
```

### 3️⃣ Using Custom Database

Initialize `AIClient` with your database implementation:

```python
from blackboxapi import AIClient
from your_module import YourCustomDatabase

custom_db = YourCustomDatabase()
client = AIClient(database=custom_db)
```

## 📚 SQLite Implementation Example

### Here's a complete example using SQLite:

```python
import sqlite3
import json
from typing import Optional
from blackboxapi.database import DatabaseInterface
from blackboxapi.models import Chat, Message

class SQLiteDatabase(DatabaseInterface):    
    def init(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS chats (
            chat_id TEXT PRIMARY KEY,
            messages TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def get_or_create_chat(self, chat_id: str) -> Chat:
        chat = self.get_chat(chat_id)
        if not chat:
            chat = Chat(self, chat_id)
            self.save_chat(chat)
        return chat

    def save_chat(self, chat: Chat) -> None:
        query = "INSERT OR REPLACE INTO chats (chat_id, messages) VALUES (?, ?)"
        messages_json = json.dumps([m.to_dict() for m in chat.get_messages()])
        self.conn.execute(query, (chat.chat_id, messages_json))
        self.conn.commit()

    def delete_chat(self, chat_id: str) -> None:
        query = "DELETE FROM chats WHERE chat_id = ?"
        self.conn.execute(query, (chat_id,))
        self.conn.commit()

    def get_chat(self, chat_id: str) -> Optional[Chat]:
        query = "SELECT messages FROM chats WHERE chat_id = ?"
        cursor = self.conn.execute(query, (chat_id,))
        row = cursor.fetchone()
        if row:
            messages_json = row[0]
            messages = [Message(m) for m in json.loads(messages_json)]
            chat = Chat(self, chat_id)
            chat.messages = messages
            return chat
        return None
```


## 🔑 Key Considerations

1. **Thread Safety**: Ensure your implementation is thread-safe if used in multi-threaded environments
2. **Error Handling**: Implement proper error handling for database operations
3. **Connection Management**: Handle database connections efficiently
4. **Data Serialization**: Properly serialize/deserialize chat messages
5. **Performance**: Consider implementing caching for frequently accessed chats

## 💡 Best Practices

- Use connection pooling for better performance
- Implement proper logging for debugging
- Add data validation before saving
- Consider implementing backup mechanisms
- Use prepared statements to prevent SQL injection
- Handle database migrations gracefully

## 🚀 Advanced Features

Consider implementing these additional features:

- Chat message pagination
- Message search functionality
- Chat metadata storage
- User session management
- Analytics data collection

## 🔍 Debugging Tips

1. Enable debug logging in your database implementation:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(name)

def save_chat(self, chat: Chat) -> None:
    logger.debug(f"Saving chat {chat.chat_id}")
    # Implementation
```

2. Add data validation:

```python
def validate_chat(self, chat: Chat) -> bool:
    if not chat.chat_id:
        raise ValueError("Chat ID cannot be empty")
    if not chat.get_messages():
        logger.warning(f"Saving empty chat: {chat.chat_id}")
    return True
```

---

<p align="center">Need help? Check out our <a href="https://github.com/Keva1z/BlackboxAPI/issues">GitHub Issues</a>!</p>