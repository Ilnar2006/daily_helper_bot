from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from modules.weather import get_weather

router = Router()

# временное хранилище городов (можно потом вынести в БД)
user_cities = {}


@router.message(Command("now"))
async def weather_now(message: Message):
    city = user_cities.get(message.from_user.id)
    if not city:
        return await message.answer("Сначала напиши свой город!")
    await message.answer(get_weather(city, "now"))


@router.message(Command("tomorrow"))
async def weather_tomorrow(message: Message):
    city = user_cities.get(message.from_user.id)
    if not city:
        return await message.answer("Сначала напиши свой город!")
    await message.answer(get_weather(city, "tomorrow"))


@router.message(Command("hourly"))
async def weather_hourly(message: Message):
    city = user_cities.get(message.from_user.id)
    if not city:
        return await message.answer("Сначала напиши свой город!")
    await message.answer(get_weather(city, "hourly"))


@router.message(F.text)
async def save_city(message: Message):
    user_cities[message.from_user.id] = message.text.strip()
    await message.answer(f"✅ Запомнил твой город: {message.text}\n"
                         "Теперь можно узнать погоду:\n"
                         "/now – сейчас\n"
                         "/tomorrow – завтра\n"
                         "/hourly – по часам")
