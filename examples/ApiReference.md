# API Reference

## Completions

### create

```python
# completions.create(message: str, agent: AgentMode | None, model: Model (default: BLACKBOX), max_tokens)
# Example:
client = AIClient()
agent_mode = RU_CAN_CODER

response: str = client.completions.create("How do I code a basic HTML website?", agent_mode)
print(response)
```
Returns a string with the response from the AI.


### create_async

Not implemented yet.

### Create image

When blackbox update their image generations, i'll update this.


## Chat History

### get_chat_history

```python
# chat_history.get_chat_history(agent: AgentMode | None)
# Example:
client = AIClient()

chat_history: list[Message] = client.chat_history.get_chat_history()
for message in chat_history:
    print(f"{message.role}: {message.content}")
```
Returns a list of messages from the chat history.

### clear_chat_history

```python
# chat_history.clear_chat_history(agent: AgentMode | None)
# Example:
client = AIClient()
client.chat_history.clear_chat_history()
```
Clears the chat history for the given agent mode.

### delete_chat

```python
# chat_history.delete_chat(agent: AgentMode | None)
# Example:
client = AIClient()
client.chat_history.delete_chat()
```
Deletes the chat for the given agent mode.

## Agents

### Create your own agent

```python
# Create your own agent mode
# Example:
from blackboxapi.models import AgentMode
from blackboxapi.client import AIClient

client = AIClient()

your_agent = AgentMode(
    mode=True, # This is required, always should be True
    id="your_agent_id",
    name="Your Agent Name"
)

response = client.completions.create("Hello, how are you?", your_agent)
print(response)
```
To get your agent id, go to the [Blackbox AI](https://blackbox.ai/) and create your own agent, then copy the id from the url. It will look like this: `https://blackbox.ai/agent/your_agent_id`.

## Thats all!
