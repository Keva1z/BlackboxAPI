from blackboxapi.client import AIClient
from blackboxapi.models import AgentMode

client = AIClient()

agent_mode = AgentMode(mode=True, id="CANCoderwFvlqld", name="CAN Coder")

# Первое сообщение
response = client.generate("How do I code the basic HTML website?", agent_mode)
print("Assistant:", response)

# Второе сообщение в том же чате
response = client.generate("Can you show me an example?", agent_mode)
print("Assistant:", response)

# Вывод истории чата
print("\nChat History:")
for message in client.get_chat_history():
    print(f"{message.role}: {message.content}")
