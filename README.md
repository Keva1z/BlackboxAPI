# BlackboxAPI

<div align="center">

![Version](https://img.shields.io/badge/version-0.3.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
[![Documentation](https://img.shields.io/badge/docs-examples-brightgreen.svg)](examples/)

A powerful Python library for interacting with the Blackbox AI API, supporting multiple AI models and specialized agents.

[Installation](#installation) •
[Quick Start](#quick-start) •
[Features](#features) •
[Documentation](#documentation) •
[Examples](#examples)

</div>

## 🚀 Installation

```bash
pip install blackboxapi
```

## 🚀 Quick Start

```python
from blackboxapi import AIClient, RU_CAN_CODER, CLAUDE

client = AIClient(logging=True) #Initialize the client

# Generate with Russian-speaking coding agent
response = client.completions.create(
    "How do I create a REST API with FastAPI?",
    agent=RU_CAN_CODER,
    model=CLAUDE # This is not used by the agent, but can be specified
)

print("Assistant:", response)

# Access chat history
print("\nChat History:") 
for message in client.get_chat_history():
    print(f"{message.role}: {message.content}")
```

## ✨ Features

- 🤖 Support for multiple AI models:
  - GPT-4
  - Claude
  - Gemini
  - Blackbox AI

- 🎭 Specialized agent modes:
  - Prompt Generator
  - Russian-speaking Coding Assistant
  - Russian-speaking Relationship Coach
  - Russian-speaking Mental Health Advisor
  - Russian-speaking Algorithm Expert
  - Russian-speaking IT Expert
  - Russian-speaking Math Teacher
  - Russian-speaking Math Expert

- 💾 Flexible database integration:
  - Built-in in-memory storage
  - Custom database support
  - Chat history management
  - Metadata tracking

- 🔄 Async support:
  - Asynchronous API calls
  - Non-blocking operations
  - High performance

- 🛠️ Advanced features:
  - Detailed logging
  - Error handling
  - Cookie management
  - Request customization
  - Response processing

## 📖 Documentation

- [Getting Started](examples/HowToGetCookie.md)
- [Database Integration](examples/HowToDB.md)
- [API Reference](examples/ApiReference.md)
- [Code Examples](tests/)

## 💡 Examples

### Basic Usage

```python
from blackboxapi import AIClient, CLAUDE
client = AIClient(logging=True)
response = client.completions.create(
    "Explain Python decorators",
    model=CLAUDE
)
print(response)
```

### Using Agent Modes

```python
from blackboxapi import AIClient, RU_CAN_CODER, CLAUDE
client = AIClient(logging=True)
response = client.completions.create(
    "How do I create a REST API with FastAPI?",
    agent=RU_CAN_CODER,
    model=CLAUDE
)
```

### Async Operations

```python
import asyncio
from blackboxapi import AIClient, RU_ALGORITHM_EXPLAINER
async def main():
    client = AIClient()
    response = await client.completions.create_async(
        "Explain quicksort algorithm",
        agent=RU_ALGORITHM_EXPLAINER
    )
    print(response)
    
asyncio.run(main())
```

## 🔧 Configuration

The library can be configured through various parameters:

```python
from blackboxapi import AIClient
client = AIClient(
    base_url="https://www.blackbox.ai",
    cookie_file="cookies.json",
    use_chat_history=True,
    database=None, # Custom database implementation
    logging=True # Enable detailed logging
)
```


## 🔑 Authentication

BlackboxAPI requires authentication via cookie. Two options are available:

1. Create a `cookies.json` file in your project directory
2. Enter the cookie string when prompted (will be saved automatically)

See [Cookie Guide](examples/HowToGetCookie.md) for detailed instructions.

## 🤖 Available Models

| Model | Max Tokens | Streaming | Languages |
|-------|------------|-----------|-----------|
| GPT-4 | 8192 | ❌ | Multi |
| Claude | 8192 | ❌ | Multi |
| Gemini | 4096 | ❌ | Multi |
| Blackbox | 2048 | ❌ | EN, RU |

## 🎭 Agent Modes

| Agent | Description | Languages |
|-------|-------------|-----------|
| PROMPT_GENERATOR | Creates optimized prompts | EN |
| RU_CAN_CODER | Coding assistant | RU |
| RU_RELATIONSHIP_COACH | Relationship advisor | RU |
| RU_MENTAL_ADVISOR | Mental health advisor | RU |
| RU_ALGORITHM_EXPLAINER | Algorithm expert | RU |
| RU_IT_EXPERT | IT professional | RU |
| RU_MATH_TEACHER | Math teacher | RU |
| RU_MATH_EXPERT | Advanced math expert | RU |

## 📊 Error Handling

```python
from blackboxapi import AIClient, APIError
client = AIClient()
try:
    response = client.completions.create("Your prompt")
except APIError as e:
    print(f"API Error: {e}")
except Exception as e:
    print(f"Error: {e}")
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

- Author: Keva1z
- Email: Keva1z@yandex.ru
- GitHub: [Keva1z/blackboxapi](https://github.com/Keva1z/blackboxapi)

---

<p align="center">Made with ❤️ by Keva1z</p>