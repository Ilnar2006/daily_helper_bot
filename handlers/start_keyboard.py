from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


"""
КЛАВИАТУРЫ ДЛЯ РЕГИСТРАЦИИ И ГЛАВНОГО МЕНЮ ДЛЯ ФАЙЛА start.py
"""

# ========== КЛАВИАТУРЫ И КНОПКИ ==========

# ========== пол ==========
def gender_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="♂ Мужской", callback_data="gender_m")],
            [InlineKeyboardButton(text="♀ Женский", callback_data="gender_f")]
        ]
    )

# ========== кнопка отправки локации ==========
send_location_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📍 Отправить местоположение", request_location=True)],
        [KeyboardButton(text="➡️ Пропустить")]
    ],
    
    resize_keyboard=True, 
    one_time_keyboard=True,
    input_field_placeholder="Нажми, чтобы отправить местоположение"
    )

# ========== соц. статус ==========
def social_status_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Школьник", callback_data="social_status_schoolboy")],
            [InlineKeyboardButton(text="Студент", callback_data="social_status_student")],
            [InlineKeyboardButton(text="Рабочий", callback_data="social_status_worker")],
            [InlineKeyboardButton(text="Безработный", callback_data="social_status_unemployed")],
            [InlineKeyboardButton(text="Другое", callback_data="social_status_other")],
        ]
    )

# ========== подтверждение данных регистрации ==========
def confirm_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Всё верно", callback_data="confirm_yes")],
            [InlineKeyboardButton(text="✏ Изменить", callback_data="confirm_edit")]
        ]
    )

# ========== главное меню после регистрации ==========
def main_menu_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌤 Погода", callback_data="menu_weather")],
            [InlineKeyboardButton(text="📅 Планировщик", callback_data="menu_todo")],
            [InlineKeyboardButton(text="🤖 AI помощник", callback_data="menu_ai")]
        ]
    )
