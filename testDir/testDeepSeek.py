import requests
import os

API_KEY = os.environ.get("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "user", "content": "Привет, расскажи что такое DeepSeek."}
    ],
    "temperature": 0.7
}

response = requests.post(API_URL, headers=headers, json=data)

if response.ok:
    result = response.json()
    print(result["choices"][0]["message"]["content"])
else:
    print("Ошибка:", response.status_code, response.text)
