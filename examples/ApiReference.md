# 📚 BlackboxAPI Reference

<div align="center">

![Version](https://img.shields.io/badge/version-0.3.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

Comprehensive API reference for the BlackboxAPI library.

</div>

## 📋 Table of Contents

- [Client Configuration](#client-configuration)
- [Completions API](#completions-api)
- [Chat Management](#chat-management)
- [Models](#models)
- [Agent Modes](#agent-modes)
- [Database Integration](#database-integration)
- [Error Handling](#error-handling)
- [Utilities](#utilities)

## 🔧 Client Configuration

### Initializing the Client

```python
from blackboxapi import AIClient

client = AIClient(
    base_url="https://www.blackbox.ai",    # API endpoint
    cookie_file="cookies.json",            # Path to cookie file
    use_chat_history=True,                 # Enable chat history
    database=None,                         # Custom database implementation
    logging=True                           # Enable detailed logging
)
```

### Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| base_url | str | "https://www.blackbox.ai" | API endpoint URL |
| cookie_file | Optional[str] | None | Path to cookie file |
| use_chat_history | bool | True | Enable chat history |
| database | Optional[DatabaseInterface] | None | Custom database |
| logging | bool | False | Enable logging |

## 🚀 Completions API

### Synchronous Generation

```python
from blackboxapi import AIClient, RU_CAN_CODER, CLAUDE

client = AIClient()
response = client.completions.create(
    message="How do I implement a binary tree?",
    agent=RU_CAN_CODER,          # Optional agent mode
    model=CLAUDE,                # Optional model selection
    max_tokens=1024             # Optional token limit
)
```

### Asynchronous Generation

```python
import asyncio
from blackboxapi import AIClient

client = AIClient()
response = await client.completions.create_async(
    message="Explain async/await in Python",
    agent=None,                 # Optional agent mode
    model=CLAUDE,               # Optional model selection
    max_tokens=2048            # Optional token limit
)
```

## 💬 Chat Management

### Accessing Chat History

```python
# Get chat history for default chat
messages = client.get_chat_history()

# Get chat history for specific agent
messages = client.get_chat_history(agent=RU_CAN_CODER)

# Access message details
for message in messages:
    print(f"{message.role}: {message.content}")
    print(f"ID: {message.id}")
    print(f"Timestamp: {message.timestamp}")
```

### Managing Chats

```python
# Clear chat history
client.clear_chat_history(agent=RU_CAN_CODER)

# Delete chat completely
client.delete_chat(agent=RU_CAN_CODER)
```

## 🤖 Models

### Available Models

```python
from blackboxapi import GPT4, CLAUDE, GEMINI, BLACKBOX

# Model capabilities
print(GPT4.max_tokens)        # 8192
print(CLAUDE.max_tokens)      # 8192
print(GEMINI.max_tokens)      # 4096
print(BLACKBOX.max_tokens)    # 2048
```

### Model Properties

| Model | ID | Max Tokens | Streaming |
|-------|------|------------|-----------|
| GPT4 | gpt-4o | 8192 | ❌ |
| CLAUDE | claude-3.5-sonnet | 8192 | ❌ |
| GEMINI | gemini-pro | 4096 | ❌ |
| BLACKBOX | blackbox-ai | 2048 | ❌ |

## 🎭 Agent Modes

### Available Agents

```python
from blackboxapi import (
    PROMPT_GENERATOR,
    RU_CAN_CODER,
    RU_RELATIONSHIP_COACH,
    RU_MENTAL_ADVISOR,
    RU_ALGORITHM_EXPLAINER,
    RU_IT_EXPERT,
    RU_MATH_TEACHER,
    RU_MATH_EXPERT
)

# Get agent by ID
from blackboxapi import get_agent_by_id
agent = get_agent_by_id("CANCoderwFvlqld")

# Get agent by name
from blackboxapi import get_agent_by_name
agent = get_agent_by_name("CAN Coder")
```

### Agent Properties

```python
# Access agent properties
print(RU_CAN_CODER.name)        # "CAN Coder"
print(RU_CAN_CODER.id)          # "CANCoderwFvlqld"
print(RU_CAN_CODER.description) # "Russian-speaking coding assistant..."
```

## 💾 Database Integration

### Custom Database Implementation

```python
from blackboxapi import DatabaseInterface, Chat
from typing import Optional, List

class CustomDatabase(DatabaseInterface):
    def get_or_create_chat(self, chat_id: str) -> Chat:
        # Implementation
        pass
        
    def save_chat(self, chat: Chat) -> None:
        # Implementation
        pass
        
    def delete_chat(self, chat_id: str) -> None:
        # Implementation
        pass
        
    def get_chat(self, chat_id: str) -> Optional[Chat]:
        # Implementation
        pass
        
    def list_chats(self) -> List[str]:
        # Implementation
        pass

# Use custom database
client = AIClient(database=CustomDatabase())
```

### Built-in Database

```python
from blackboxapi import DictDatabase

# In-memory database (default)
database = DictDatabase()

# Access metadata
metadata = database.get_chat_metadata(chat_id)
print(metadata["created_at"])
print(metadata["message_count"])
print(metadata["last_updated"])

# Clear database
database.clear_all()
```

## ⚠️ Error Handling

```python
from blackboxapi import AIClient, APIError, DatabaseError

client = AIClient()

try:
    response = client.completions.create("Your prompt")
except APIError as e:
    print(f"API Error: {e}")
except DatabaseError as e:
    print(f"Database Error: {e}")
except Exception as e:
    print(f"Unexpected Error: {e}")
```

## 🛠️ Utilities

### Cookie Management

```python
from blackboxapi.utils import (
    load_cookies,
    parse_and_save_cookies,
    validate_cookie,
    get_cookie_expiration
)

# Load cookies
cookies = load_cookies("cookies.json")

# Validate cookie string
is_valid = validate_cookie(cookie_string)

# Save cookies
cookie_dict = parse_and_save_cookies(cookie_string, "cookies.json")

# Check expiration
expiration = get_cookie_expiration(cookie_dict)
```

### Logging

```python
client = AIClient(logging=True)

# Log levels are automatically colored:
# - INFO: Cyan
# - WARNING: Yellow
# - ERROR: Red
# - REQUEST: Magenta
# - RESPONSE: Green
# - DEBUG: Blue
```

## 📝 Type Hints

The library provides comprehensive type hints for better IDE support:

```python
from blackboxapi.models import Message, Chat, AgentMode, Model
from typing import List, Optional, Dict, Any

def process_messages(
    messages: List[Message],
    agent: Optional[AgentMode] = None
) -> Dict[str, Any]:
    # Your code with full type support
    pass
```

---

<p align="center">For more examples, visit our <a href="https://github.com/Keva1z/blackboxapi">GitHub repository</a></p>