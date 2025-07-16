import os
import requests
import telebot
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util

# --- Конфигурация ---
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions'

# --- Telegram Bot ---
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# --- Загрузка модели ---
model = SentenceTransformer("all-MiniLM-L6-v2")

# --- Загрузка услуг ---
df = pd.read_csv("rag_services.csv")
services = df["Услуга"].tolist()

# --- Кэширование эмбеддингов ---
embedding_cache_path = "service_embeddings.pt"
if os.path.exists(embedding_cache_path):
    print("Загружаем эмбеддинги из кеша...")
    service_embeddings = torch.load(embedding_cache_path)
else:
    print("Создаём эмбеддинги заново...")
    service_embeddings = model.encode(services, convert_to_tensor=True)
    torch.save(service_embeddings, embedding_cache_path)

print(f"Загружено {len(services)} услуг. Эмбеддинги: {service_embeddings.shape}")

# --- Обработка сообщений ---
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text

    # Поиск релевантной услуги
    try:
        query_embedding = model.encode(user_text, convert_to_tensor=True)
        cos_scores = util.pytorch_cos_sim(query_embedding, service_embeddings)[0]
        top_result = cos_scores.argmax()
        matched_service = services[top_result]
        print(f"Запрос: {user_text} → Услуга: {matched_service}")
    except Exception as e:
        matched_service = "Не удалось определить услугу по сообщению."
        print(f"Ошибка семантического поиска: {e}")

    # Сборка запроса к DeepSeek
    prompt = (
        f"Ты — сервисный ассистент. Пользователь написал: '{user_text}'.\n"
        f"Сравнив это сообщение с каталогом услуг, была найдена наиболее релевантная услуга: '{matched_service}'.\n"
        f"Ответь так, будто ты предлагаешь именно эту услугу. Подробно и понятно опиши, что она включает."
    )

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        answer = result['choices'][0]['message']['content']
    except Exception as e:
        answer = f"Ошибка запроса к DeepSeek: {e}"

    bot.send_message(message.chat.id, answer)

# --- Запуск ---
print("Бот запущен...")
bot.infinity_polling()
