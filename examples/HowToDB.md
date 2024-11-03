# 💾 Database Integration Guide

<div align="center">

![Version](https://img.shields.io/badge/version-0.3.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

A comprehensive guide to implementing custom database solutions for BlackboxAPI.

</div>

## 📋 Table of Contents

- [Overview](#overview)
- [Built-in Database](#built-in-database)
- [Custom Implementation](#custom-implementation)
- [Database Interface](#database-interface)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## 📖 Overview

BlackboxAPI provides a flexible database interface for storing chat histories and metadata. You can:

- Use the built-in in-memory database
- Implement your own storage solution
- Handle persistence and caching
- Track chat metadata

## 🔧 Built-in Database

The default `DictDatabase` provides in-memory storage:

```python
from blackboxapi import AIClient, DictDatabase

# Using default database
client = AIClient()

# Explicitly creating database
database = DictDatabase()
client = AIClient(database=database)

# Accessing metadata
chat_id = "some_chat_id"
metadata = database.get_chat_metadata(chat_id)
print(f"Messages: {metadata['message_count']}")
print(f"Created: {metadata['created_at']}")
print(f"Updated: {metadata['last_updated']}")
```

## 🛠️ Custom Implementation

### Basic Example

```python
from blackboxapi import DatabaseInterface, Chat
from typing import Optional, List, Dict, Any
import sqlite3

class SQLiteDatabase(DatabaseInterface):
    def __init__(self, db_path: str = "chats.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS chats (
                    chat_id TEXT PRIMARY KEY,
                    messages TEXT,
                    created_at TEXT,
                    last_updated TEXT
                )
            """)
    
    def get_or_create_chat(self, chat_id: str) -> Chat:
        try:
            chat = self.get_chat(chat_id)
            if not chat:
                chat = Chat(self, chat_id)
                self.save_chat(chat)
            return chat
        except Exception as e:
            raise DatabaseError(f"Database error: {str(e)}")
    
    # Implement other required methods...
```

### Advanced Example

```python
from blackboxapi import DatabaseInterface, Chat
import redis
import json

class RedisDatabase(DatabaseInterface):
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis = redis.Redis(host=host, port=port, db=db)
        
    def get_or_create_chat(self, chat_id: str) -> Chat:
        try:
            chat_data = self.redis.get(f"chat:{chat_id}")
            if chat_data:
                # Deserialize and create chat
                data = json.loads(chat_data)
                chat = Chat(self, chat_id)
                for msg in data['messages']:
                    chat.add_message(msg['content'], msg['role'])
                return chat
            else:
                # Create new chat
                chat = Chat(self, chat_id)
                self.save_chat(chat)
                return chat
        except Exception as e:
            raise DatabaseError(f"Redis error: {str(e)}")
```

## 📝 Database Interface

The `DatabaseInterface` requires implementing these methods:

```python
class DatabaseInterface(ABC):
    @abstractmethod
    def get_or_create_chat(self, chat_id: str) -> Chat:
        """Get existing chat or create new one."""
        pass

    @abstractmethod
    def save_chat(self, chat: Chat) -> None:
        """Save chat to storage."""
        pass

    @abstractmethod
    def delete_chat(self, chat_id: str) -> None:
        """Delete chat from storage."""
        pass

    @abstractmethod
    def get_chat(self, chat_id: str) -> Optional[Chat]:
        """Retrieve chat from storage."""
        pass

    @abstractmethod
    def list_chats(self) -> List[str]:
        """List all chat IDs."""
        pass
```

## 💡 Examples

### MongoDB Integration

```python
from blackboxapi import DatabaseInterface, Chat
from pymongo import MongoClient
from datetime import datetime

class MongoDatabase(DatabaseInterface):
    def __init__(self, uri: str = "mongodb://localhost:27017"):
        self.client = MongoClient(uri)
        self.db = self.client.blackbox
        self.chats = self.db.chats
        
    def save_chat(self, chat: Chat) -> None:
        chat_data = {
            "chat_id": chat.chat_id,
            "messages": [m.to_dict() for m in chat.get_messages()],
            "metadata": {
                "message_count": len(chat.get_messages()),
                "last_updated": datetime.utcnow().isoformat()
            }
        }
        self.chats.update_one(
            {"chat_id": chat.chat_id},
            {"$set": chat_data},
            upsert=True
        )
```

### PostgreSQL Integration

```python
from blackboxapi import DatabaseInterface, Chat
import psycopg2
import json

class PostgresDatabase(DatabaseInterface):
    def __init__(self, dsn: str):
        self.dsn = dsn
        self._init_db()
        
    def _init_db(self):
        with psycopg2.connect(self.dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS chats (
                        chat_id TEXT PRIMARY KEY,
                        messages JSONB,
                        metadata JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
```

## ✅ Best Practices

1. **Error Handling**
   - Always wrap database operations in try/except blocks
   - Raise `DatabaseError` with meaningful messages
   - Log errors for debugging

2. **Performance**
   - Implement caching for frequently accessed chats
   - Use connection pooling for SQL databases
   - Batch operations when possible

3. **Data Integrity**
   - Validate data before saving
   - Implement backup strategies
   - Use transactions where appropriate

4. **Security**
   - Sanitize inputs
   - Use parameterized queries
   - Implement proper access controls

## ❗ Troubleshooting

Common issues and solutions:

1. **Connection Errors**
   ```python
   try:
       # Your database operation
   except ConnectionError as e:
       logger.error(f"Database connection failed: {e}")
       # Implement retry logic
   ```

2. **Data Corruption**
   ```python
   def validate_chat_data(self, chat: Chat) -> bool:
       """Validate chat data before saving."""
       if not chat.chat_id:
           raise ValueError("Chat ID is required")
       # Add more validation...
   ```

3. **Performance Issues**
   ```python
   from functools import lru_cache
   
   class CachedDatabase(DatabaseInterface):
       @lru_cache(maxsize=100)
       def get_chat(self, chat_id: str) -> Optional[Chat]:
           # Implementation with caching
           pass
   ```

---

<p align="center">Need help? Join our <a href="https://github.com/Keva1z/blackboxapi/discussions">discussions</a>!</p>