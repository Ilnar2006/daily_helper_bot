"""
Клавиатуры для модуля погоды.
"""

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

def get_weather_menu() -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру с кнопкой для получения прогноза погоды.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            InlineKeyboardButton(text="Погода на сегодня", callback_data="weather_for_today"),
            InlineKeyboardButton(text="Погода на завтра", callback_data="weather_for_tomorrow"),
            InlineKeyboardButton(text="Погода на 3 дня", callback_data="weather_for_3_days"),
            InlineKeyboardButton(text="Погода на неделю", callback_data="weather_for_week")
        ]
    )