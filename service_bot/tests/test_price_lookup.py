from app.services.vector_db import search_service_price
from app.services.vector_db import VectorDB

def test_existing_service():
    result = search_service_price("замена масла")
    assert result is not None

def test_non_existing_service():
    result = search_service_price("непонятная услуга")
    assert result is None

def test_vector_search():
    db = VectorDB("data/rag_services.csv")
    result = db.search("замена масла")
    assert "моторного масла" in result["Услуга"].lower()