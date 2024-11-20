import sys
import os
import asyncio

# Добавляем путь к исходному коду в PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from blackboxapi.client import AIClient
from blackboxapi.agent import RU_CAN_CODER

async def main():
    client = AIClient(enable_logging=True)
    agent_mode = RU_CAN_CODER

    while True:
        prompt = input(">> ")
        if prompt == "//": break
        
        response = await client.completions.create_async(prompt, max_tokens=90000)
        print("Assistant:", response)

asyncio.run(main())