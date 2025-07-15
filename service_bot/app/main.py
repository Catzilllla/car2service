import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from app.configs import config
from app.handlers import user_flow, price_lookup


async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(user_flow.router, price_lookup.router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())