# 🤖 BlackboxAPI

A powerful Python library for seamless interaction with the Blackbox AI API. Leverage multiple AI models and agent modes with an elegant, developer-friendly interface.

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## ✨ Features

- 🚀 Intuitive and powerful client interface
- 🤖 Support for multiple AI models (GPT-4, Claude, Gemini, Blackbox AI)
- 🎭 Customizable agent modes with specialized capabilities
- 💾 Built-in chat history management
- 🍪 Automatic cookie handling and validation
- 🔄 Async support for high-performance applications
- 🌐 Can see pages that you give to him

## 📦 Installation

```bash
pip install git+https://github.com/Keva1z/BlackboxAPI.git
```

## 🚀 Quick Start

```python
from blackboxapi import AIClient, AgentMode
from blackboxapi.agent import RU_CAN_CODER

client = AIClient() #Initialize the client

agent_mode = RU_CAN_CODER # Select an agent mode
response = client.completions.create(
    "How do I create a REST API with FastAPI?",
    agent_mode
) # Generate a response

print("Assistant:", response)
print("\nChat History:") 
for message in client.get_chat_history(): # Access chat history
    print(f"{message.role}: {message.content}")
```

## 📚 Documentation

- [🍪 How to Get Cookie](examples/HowToGetCookie.md)
- [💾 Custom Database Integration](examples/HowToDB.md)
- [📝 Code Examples](tests/test_dialogue.py)
- [🎭 Available Agent Modes](blackboxapi/agent.py)
- [📖 API Reference](examples/ApiReference.md)

## ⚙️ Configuration

BlackboxAPI requires authentication via cookie. Two options are available:

1. Create a `cookies.json` file in your project directory
2. Enter the cookie string when prompted (will be saved automatically)

## 🤖 Available Models

- GPT-4
- Claude
- Gemini
- Blackbox AI

## 🎭 Agent Modes

Specialized agents for different tasks:

- `PROMPT_GENERATOR` - Creates optimized prompts
- `CAN_CODER` - Russian-speaking coding assistant
- `MENTAL_ADVISOR` - Russian-speaking mental health advisor
- `ALGORITHM_EXPLAINER` - Russian-speaking algorithm expert
- `RELATIONSHIP_COACH` - Russian-speaking relationship advisor

Create custom agents by extending the `AgentMode` class!

## 🤝 Contributing

Contributions are always welcome! Feel free to:

1. Fork the repository
2. Create a feature branch
3. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [Blackbox AI](https://www.blackbox.ai) for providing the core AI services
- All contributors who help improve this library

---

<p align="center">Made with ❤️ by Keva1z</p>