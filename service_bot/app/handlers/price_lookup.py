# from aiogram import Router, types
# from app.services.vector_db import search_service_price

# router = Router()

# @router.message()
# async def handle_price_query(message: types.Message):
#     query = message.text.strip().lower()
#     price = search_service_price(query)
#     if price:
#         await message.answer(f"{price['Услуга']} стоит {price['Цена (₽)']} ₽")
#     else:
#         await message.answer("К сожалению, такой услуги нет в прайс-листе.")


# app/handlers/price_lookup.py
from aiogram import Router
from aiogram.types import Message
from app.services.vector_db import VectorDB
from app.services.llm_client import query_deepseek

router = Router()
vector_db = VectorDB("data/rag_services.csv")  # путь к файлу

@router.message()
async def handle_question(message: Message):
    query = message.text.strip()
    top_match = vector_db.search(query)
    context = f"{top_match['Услуга']}: {top_match['Цена (₽)']} ₽"

    try:
        answer = await query_deepseek(context, query)
    except Exception as e:
        answer = "Ошибка при обращении к LLM. Попробуйте позже."

    await message.answer(answer)
