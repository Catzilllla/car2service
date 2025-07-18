import os
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util
from datetime import datetime
from colorama import init, Fore, Style

# Инициализация colorama
init(autoreset=True)

# --- Загрузка данных ---
df = pd.read_csv("rag_services.csv")
services = df["Услуга"].tolist()

# --- Загрузка модели ---
model = SentenceTransformer("all-MiniLM-L6-v2")

# --- Эмбеддинги с кешем ---
embedding_cache_path = "service_embeddings.pt"
device = "cuda" if torch.cuda.is_available() else "cpu"

if os.path.exists(embedding_cache_path):
    print(Fore.YELLOW + "🔄 Загружаем эмбеддинги из кеша...")
    service_embeddings = torch.load(embedding_cache_path).to(device)
else:
    print(Fore.CYAN + "🔧 Создаём эмбеддинги заново...")
    service_embeddings = model.encode(services, convert_to_tensor=True, device=device)
    torch.save(service_embeddings, embedding_cache_path)

print(Fore.GREEN + f"✅ Загружено {len(services)} услуг. Эмбеддинги: {service_embeddings.shape}")

# --- Поиск услуги ---
def search_service(query, threshold=0.45):
    query_embedding = model.encode(query, convert_to_tensor=True).to(device)
    cos_scores = util.pytorch_cos_sim(query_embedding, service_embeddings)[0]

    top_score = torch.max(cos_scores).item()
    top_idx = torch.argmax(cos_scores).item()

    if top_score >= threshold:
        service = services[top_idx]
        price = df.iloc[top_idx]["Стоимость (руб.)"]
        return {
            "match_found": True,
            "услуга": service,
            "стоимость": f"{int(price)} руб.",
            "score": top_score
        }
    else:
        return {
            "match_found": False,
            "таблица": df.to_dict(orient="records"),
            "score": top_score
        }

# --- Логгирование ---
def log_interaction(query, result):
    with open("rag_log.txt", "a", encoding="utf-8") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] Запрос: {query}\n")
        if result["match_found"]:
            log_file.write(f"  Найдена: {result['услуга']} — {result['стоимость']}, score={result['score']:.2f}\n")
        else:
            log_file.write(f"  Ничего не найдено, score={result['score']:.2f}\n")
        log_file.write("-" * 40 + "\n")

# --- Основной цикл ---
print(Fore.BLUE + "\n🤖 RAG-помощник по автосервису.\nНапиши, что тебе нужно. Напиши 'выход' для завершения.")

while True:
    query = input(Fore.WHITE + "\n🧑‍🔧 Ваш запрос: ").strip()
    if query.lower() in ["выход", "exit", "quit"]:
        print(Fore.MAGENTA + "👋 До свидания!")
        break

    result = search_service(query)
    log_interaction(query, result)

    if result["match_found"]:
        print(Fore.GREEN + f"\n✅ Найдена услуга: {result['услуга']}")
        print(Fore.YELLOW + f"💰 Стоимость: {result['стоимость']}")
        print(Fore.CYAN + f"📈 Семантическая близость: {result['score']:.2f}")
    else:
        print(Fore.RED + "\n⚠️ Услуга не найдена. Вот доступные услуги:")
        for row in result["таблица"]:
            print(Fore.LIGHTBLACK_EX + f"- {row['Услуга']} — {row['Стоимость (руб.)']} руб.")
        print(Fore.CYAN + f"\n📉 Семантическая близость: {result['score']:.2f}")
