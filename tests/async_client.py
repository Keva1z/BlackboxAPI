import asyncio
from blackboxapi.client import AIClient
from blackboxapi.agent import RU_CAN_CODER

async def main():
    client = AIClient(logging=True)
    agent_mode = RU_CAN_CODER

    while True:
        prompt = input(">> ")
        if prompt == "//": break
        
        response = await client.completions.create_async(prompt, agent_mode, max_tokens=90000)
        print("Assistant:", response)

asyncio.run(main())