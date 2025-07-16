import pandas as pd
from sentence_transformers import SentenceTransformer, util
import torch

# === 1. Загрузка данных ===
csv_path = "rag_services.csv"
df = pd.read_csv(csv_path)
services = df["Услуга"].tolist()

# === 2. Модель для эмбеддингов ===
model = SentenceTransformer("all-MiniLM-L6-v2")
service_embeddings = model.encode(services, convert_to_tensor=True)

# === 3. Поисковая функция ===
def search_service(query, threshold=0.45):
    query_embedding = model.encode(query, convert_to_tensor=True)
    cos_scores = util.pytorch_cos_sim(query_embedding, service_embeddings)[0]

    # Находим лучший результат
    top_score = torch.max(cos_scores).item()
    top_idx = torch.argmax(cos_scores).item()

    if top_score >= threshold:
        service = services[top_idx]
        price = df.iloc[top_idx]["Стоимость (руб.)"]
        return {
            "match_found": True,
            "услуга": service,
            "стоимость": f"{int(price)} руб."
        }
    else:
        return {
            "match_found": False,
            "таблица": df.to_dict(orient="records")
        }

# === 4. Тестовый пример ===
if __name__ == "__main__":
    user_query = input("Введите ваш запрос: ")
    result = search_service(user_query)

    if result["match_found"]:
        print(f"\nНайдена услуга:\n- {result['услуга']}\n- Стоимость: {result['стоимость']}")
    else:
        print("\nУслуга не найдена. Доступные услуги и цены:")
        for row in result["таблица"]:
            print(f"- {row['Услуга']} — {row['Стоимость (руб.)']} руб.")
