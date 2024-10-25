from blackboxapi.client import AIClient
from blackboxapi.models import AgentMode
from blackboxapi.agent import RU_CAN_CODER

client = AIClient()

# Use your own agent mode
# agent_mode = AgentMode(mode=True, id="CANCoderwFvlqld", name="CAN Coder")

agent_mode = RU_CAN_CODER

# Generate with agent:
response = client.generate("How do I code the basic HTML website?", agent_mode)
print("Assistant:", response)

# Generate without agent:
response = client.generate("Can you show me an example?", agent_mode)
print("Assistant:", response)

# Show chat history for agent:
print("\nChat History (with agent):")
for message in client.get_chat_history(agent_mode):
    print(f"{message.role}: {message.content}")

# Show chat history without agent:
print("\nChat History (without agent):")
for message in client.get_chat_history(None):
    print(f"{message.role}: {message.content}")
