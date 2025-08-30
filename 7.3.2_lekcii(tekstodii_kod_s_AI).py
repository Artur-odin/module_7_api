#Тестовый код с https://github.com/gpt4free/gpt4free.github.io/blob/main/docs/async_client.md 

#Вывод сразу полностью готового ответа

import asyncio
from g4f.client import AsyncClient

async def main():
    client = AsyncClient()
    
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": "Какая сейчас погода в Австралии?"
            }
        ],
        web_search = False #False - не ищет в интернете, True - ищет в интернете
    )
    
    print(response.choices[0].message.content)

asyncio.run(main())       
