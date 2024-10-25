# BlackboxAPI

BlackboxAPI is a Python library for interacting with the Blackbox AI API. It provides a simple and efficient way to generate responses using various AI models and agent modes.

## Features

- Easy-to-use client for Blackbox AI API
- Support for multiple AI models (GPT-4, Claude, Gemini, Blackbox AI)
- Customizable agent modes
- Chat history management
- Automatic cookie handling and validation

## Installation

You can install BlackboxAPI using pip:

```bash
pip install git+https://github.com/Keva1z/BlackboxAPI.git
```

## Usage

Here's a basic example of how to use BlackboxAPI:

```python
from blackboxapi import AIClient, AgentMode
from blackboxapi.agent import RU_CAN_CODER

client = AIClient() # Initialize the client

agent_mode = RU_CAN_CODER # Use a specific agent mode

# Generate a response
response = client.completions.create("How do I code a basic HTML website?", agent_mode)
print("Assistant:", response)

print("\nChat History:") # Get chat history

for message in client.get_chat_history():
    print(f"{message.role}: {message.content}")
```

- [How to get cookie](examples/HowToGetCookie.md)
- [How to use custom database](examples/HowToDB.md)
- [More examples](tests/test_dialogue.py)
- [All agent modes](blackboxapi/agent.py)
- [API Reference](examples/ApiReference.md)

## Configuration

BlackboxAPI requires a valid cookie for authentication. You can provide the cookie in two ways:

1. Create a `cookies.json` file in your project directory with the required cookie information.
2. When prompted, enter the cookie string manually, and the library will save it for future use.

## Available Models

BlackboxAPI supports the following AI models:

- GPT-4o
- Claude
- Gemini
- Blackbox AI

## Agent Modes

You can use predefined agent modes or create custom ones:

- PROMPT_GENERATOR (Generates prompts for other agents)
- CAN_CODER (Only answer on Russian)
- MENTAL_ADVISOR (Only answer on Russian)
- ALGORITHM_EXPLAINER (Only answer on Russian)
- RELATIONSHIP_COACH (Only answer on Russian)

## API Reference

### AIClient

The main class for interacting with the Blackbox AI API.

#### Methods:

- `generate(message: str, agent_mode: AgentMode|None = None, model: Model = BLACKBOX, max_tokens=1024) -> str`
  Generate a response from the AI model.

- `get_chat_history(agent_mode: AgentMode|None = None)`
  Get the chat history for the given agent mode.

- `clear_chat_history(agent_mode: AgentMode|None = None)`
  Clear the chat history for the given agent mode.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [Blackbox AI](https://www.blackbox.ai) for providing the AI service.