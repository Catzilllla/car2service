# import pandas as pd

# df = pd.read_csv('rag_services.csv')

# def search_service_price(query: str):
#     for _, row in df.iterrows():
#         if query in row['Услуга'].lower():
#             return row.to_dict()
#     return None


# app/services/vector_db.py
from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd

class VectorDB:
    def __init__(self, path: str):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.df = pd.read_csv(path)
        self.texts = self.df["Услуга"].tolist()
        self.embeddings = self.model.encode(self.texts, convert_to_tensor=False)

    def search(self, query: str, top_k: int = 1):
        query_vec = self.model.encode([query])[0]
        scores = np.dot(self.embeddings, query_vec)  # cosine similarity
        top_idx = int(np.argmax(scores))
        return self.df.iloc[top_idx]
