import sys
import os
import asyncio
import requests
# Добавляем путь к исходному коду в PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from blackboxapi.client import AIClient, AsyncAIClient
from blackboxapi.agent import RU_CAN_CODER, RU_MENTAL_ADVISOR

from blackboxapi.utils import image_to_base64

async def main():
    client = AsyncAIClient(enable_logging=True)
    agent_mode = RU_MENTAL_ADVISOR

    # Загружаем изображение напрямую из URL
    # image_url = "https://raw.githubusercontent.com/xtekky/gpt4free/refs/heads/main/docs/cat.jpeg"
    # response = requests.get(image_url)
    # image = image_to_base64(response.content)

    image = open("tests/images/test.jpg", "rb").read()

    prompt = "Дай примерное описание характера человека на этом изображении по одежде и положению."
    response = await client.completions.create(prompt, max_tokens=1024, image=image, agent=agent_mode)
    print("Assistant:", response)

    input("Press Enter to continue...")

    prompt = "Что еще можно сказать о человеке на этом изображении?"
    response = await client.completions.create(prompt, max_tokens=1024, image=image, agent=agent_mode)
    print("Assistant:", response)

asyncio.run(main())