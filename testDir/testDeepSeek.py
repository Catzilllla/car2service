import requests

API_KEY = "sk-fff346d940fb4cc4ae1a707600084249"
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
