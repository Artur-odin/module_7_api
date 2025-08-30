#Используем системную роль для указания ИИ в какой роли он выступает

import asyncio
from g4f.client import AsyncClient

async def main():
    client = AsyncClient()

    stream = client.chat.completions.stream(
        model="gpt-4",
        messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Как тебя зовут"}
                 ],
        web_search = False
    )

    async for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="")

asyncio.run(main())