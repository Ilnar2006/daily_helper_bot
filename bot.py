import asyncio
from aiogram import Bot, Dispatcher

from utils.logger import logger

#импортируем роутреры с файлов-обработщиков
#в файлах-обработщиках создаем переменную router=Router()
from handlers.start import start_router
from handlers.help import help_router

from modules.weather.main import weather_router


from config import TOKEN

async def main():
    # await async_main()
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(help_router)
    dp.include_router(weather_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен вручную")
        #print("Бот выключен")