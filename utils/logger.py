import logging
import os

# Убедимся, что папка logs существует
os.makedirs("logs", exist_ok=True)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,  # Минимальный уровень сообщений (INFO и выше)
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler("logs/bot.log", encoding="utf-8"),  # в файл
        logging.StreamHandler()  # в консоль
    ]
)

# Экспорт логгера
logger = logging.getLogger("bot")
