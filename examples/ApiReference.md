# 📚 API Reference

Comprehensive guide to BlackboxAPI's core functionality and features.

## 🚀 Completions

### create()

**Generate AI responses synchronously.**


```python
# Signature

completions.create(
    message: str,
    agent: AgentMode | None,
    model: Model = BLACKBOX,
    max_tokens: int | None = None
) -> str
```

```python
# Example

client = AIClient()
agent_mode = RU_CAN_CODER

response: str = client.completions.create(
    "How do I code a basic HTML website?",
    agent_mode
)
print(response)
```

### create_async()

**Generate AI responses asynchronously for better performance in async applications.**

```python
# Signature

completions.create_async(
    message: str,
    agent: AgentMode | None,
    model: Model = BLACKBOX,
    max_tokens: int | None = None
) -> Coroutine[str]
```

```python
# Example

import asyncio

client = AIClient()
agent_mode = RU_CAN_CODER

async def main():
    response: str = await client.completions.create_async(
        "How do I code a basic HTML website?",
        agent_mode
    )
    print(response)

asyncio.run(main())
```

### 🎨 Create Image

> 🚧 Coming soon! Image generation features will be added when Blackbox updates their API.

## 💬 Chat History

### get_chat_history()

**Retrieve the conversation history for a specific agent or general chat.**

```python
# Signature

chat_history.get_chat_history(agent: AgentMode | None = None) -> list[Message]
```

```python
# Example

client = AIClient()

chat_history: list[Message] = client.chat_history.get_chat_history()
for message in chat_history:
    print(f"{message.role}: {message.content}")
```

### clear_chat_history()

**Reset the conversation history for a specific agent or general chat.**

```python
# Signature

chat_history.clear_chat_history(agent: AgentMode | None = None) -> None
```

```python
# Example

client = AIClient()
client.chat_history.clear_chat_history()
```

### delete_chat()

**Completely remove a chat session for a specific agent or general chat.**

```python
# Signature
chat_history.delete_chat(agent: AgentMode | None = None) -> None
```

```python
# Example

client = AIClient()
client.chat_history.delete_chat()
```

## 🤖 Custom Agents

### Creating Custom Agents

**Extend BlackboxAPI's capabilities by creating your own specialized agents.**

```python
# Example
from blackboxapi.models import AgentMode
from blackboxapi.client import AIClient

client = AIClient()

your_agent = AgentMode(
    mode=True,  # Required, always set to True
    id="your_agent_id",
    name="Your Agent Name"
)

response = client.completions.create(
    "Hello, how are you?",
    your_agent
)
print(response)
```

To obtain your agent ID:
1. Visit [Blackbox AI](https://blackbox.ai/)
2. Create a new agent
3. Copy the ID from the URL: `https://blackbox.ai/agent/your_agent_id`

## 🔑 Available Models

The following AI models are supported:

- `GPT4` - OpenAI's GPT-4
- `CLAUDE` - Anthropic's Claude
- `GEMINI` - Google's Gemini Pro
- `BLACKBOX` - Blackbox AI (default)

## 📌 Important Notes

- Always handle API responses with proper error checking
- Consider rate limits and token usage
- Store sensitive information (like cookies) securely
- Use async methods for better performance in web applications

---

<p align="center">Need more examples? Check out the <a href="https://github.com/Keva1z/BlackboxAPI/tree/main/tests">test files</a>!</p>