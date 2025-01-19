import ollama
import asyncio
from ollama import AsyncClient

resp = ollama.chat (
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": "what is 2 and 2"
        },
    ],
)
print(resp["message"]["content"])

async def chat():
    message = {
        "role": "user",
        "content": "Tell me a joke about a cat and a mouse"
    }
    async for part in await AsyncClient().chat(
        model="llama3.2", messages=[message], stream=True        
    ):
        print(part["message"]["content"], end="", flush=True)
asyncio.run(chat())