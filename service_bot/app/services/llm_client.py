# def query_llm(prompt: str) -> str:
#     return "LLM response based on: " + prompt


# app/services/llm_client.py
import os
import httpx
from app.configs import config

DEEPSEEK_API_KEY = os.getenv(config.DEEPSEEK_API_KEY)
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

async def query_deepseek(context: str, question: str) -> str:
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"Контекст: {context}\n\nВопрос: {question}"

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Ты помощник автосервиса. Отвечай по фактам из контекста."},
            {"role": "user", "content": prompt}
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(DEEPSEEK_API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
