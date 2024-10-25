# How to implement your own database for BlackboxAPI

BlackboxAPI provides a flexible interface for working with various databases. You can easily implement support for your own database by following these steps:

## 1. Create a class that implements DatabaseInterface

Your class should inherit from `DatabaseInterface` and implement all its abstract methods. Here is an example structure:

```python
from blackboxapi.database import DatabaseInterface
from blackboxapi.models import Chat
from typing import Optional

class YourCustomDatabase(DatabaseInterface):
    def init(self):
        # Initialize your database

    def get_or_create_chat(self, chat_id: str) -> Chat:
        # Logic for getting or creating a chat

    def save_chat(self, chat: Chat) -> None:
        # Logic for saving a chat

    def delete_chat(self, chat_id: str) -> None:
        # Logic for deleting a chat

    def get_chat(self, chat_id: str) -> Optional[Chat]:
        # Logic for getting a chat
```

## 2. Implement methods

Implement each method according to the logic of your database. For example:

### Get or create chat
```python
def get_or_create_chat(self, chat_id: str) -> Chat:
    chat = self.get_chat(chat_id)
    if not chat:
        chat = Chat(self, chat_id)
        self.save_chat(chat)
    return chat
```


### Save chat
```python
def save_chat(self, chat: Chat) -> None:
    # Example for a SQL-like database
    query = "INSERT OR REPLACE INTO chats (chat_id, messages) VALUES (?, ?)"
    messages_json = json.dumps([m.to_dict() for m in chat.get_messages()])
    self.execute_query(query, (chat.chat_id, messages_json))
```

## 3. Use your database with AIClient

Now you can use your custom database when initializing `AIClient`:

```python
from blackboxapi import AIClient
from your_module import YourCustomDatabase

custom_db = YourCustomDatabase()
client = AIClient(database=custom_db)
```


## Example: Implementing a SQLite database

Here is an example of implementing a database using SQLite:

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

This example demonstrates how to implement an SQLite database for storing chats and messages.

## Conclusion

Implementing your own database allows you to integrate BlackboxAPI with any data storage system you prefer. The main thing is to adhere to the `DatabaseInterface` interface and correctly implement all the necessary methods.


