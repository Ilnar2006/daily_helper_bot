#import asyncio
import logging

from config import OPENWEATHER_API_KEY

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

#from .handlers import weather_handlers
from .keyboards import get_weather_menu
from formatter import (
    format_current_weather,
    format_tomorrow_weather,
    format_weekly_forecast
)

from services import WeatherService

weather_router = Router()

# /weather команда для получения прогноза погоды
@weather_router.message(commands=["weather"])
async def cmd_weather(message: Message):
    await message.answer(
        "Выберите, какой прогноз погоды вы хотите получить:",
        reply_markup=get_weather_menu()
    )



# Обработчики inline-кнопок для прогноза погоды
@weather_router.callback_query(F.data.startswith("weather_"))
async def process_weather_callback(callback: CallbackQuery):
    """Обрабатывает нажатия на кнопки прогноза погоды."""

    lat, lon = 55.7558, 37.6176  # Москва по умолчанию

    try:
        async with WeatherService(OPENWEATHER_API_KEY) as weather_service:
            if callback.data == "weather_for_today":
                raw_data = await weather_service.get_current_weather(lat, lon)
                weather_info = format_current_weather(raw_data)
            
            elif callback.data == "weather_for_tomorrow":
                raw_data = await weather_service.get_weather_for_tomorrow(lat, lon)
                weather_info = format_tomorrow_weather(raw_data)
            
            elif callback.data == "weather_for_3_days":
                raw_data = await weather_service.get_weather_for_3_days(lat, lon)
                weather_info = format_weekly_forecast(raw_data)
            
            elif callback.data == "weather_for_week":
                raw_data = await weather_service.get_weather_for_week(lat, lon)
                weather_info = format_weekly_forecast(raw_data)
            else:
                weather_info = "Неизвестный тип прогноза."

        await callback.message.edit_text(weather_info)
    
    except Exception as e:
        logging.error(f"Ошибка при получении прогноза погоды: {e}")
        await callback.message.edit_text("Произошла ошибка при получении данных 😢")

    await callback.answer()