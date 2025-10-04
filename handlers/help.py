from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

help_router = Router()

# Главное меню справки
HELP_MAIN_TEXT = """
🤖 <b>Я — твой персональный помощник</b>  

Я умею:
- Подсказывать погоду 🌦  
- Помогать в учебе 📚  
- Работать как встроенный ИИ 🧠  
- Напоминать о делах и быть планировщиком ⏰  
- Давать полезные советы каждый день 🌟  

Выберите интересующую функцию ниже, чтобы узнать подробности.
"""

# Подробные описания функций
HELP_DETAILS = {
    "weather": """
🌦 <b>Функция: Погода</b>  

Команды:
/now — погода сейчас  
/tomorrow — погода на завтра  
/hourly — почасовой прогноз  

Я беру данные с OpenWeather API и подсказываю погоду в твоем городе.
""",
    "ai": """
🧠 <b>Функция: Встроенный ИИ</b>  

Я могу отвечать на вопросы, помогать с учебой, объяснять сложные темы простыми словами и даже помогать с кодом.  

⚡ Планируется интеграция с ChatGPT для максимальной пользы.
""",
    "planner": """
📅 <b>Функция: Планировщик</b>  

Я могу напоминать о делах, помогать планировать день и мотивировать.  

(В разработке: ежедневные задачи, напоминания, уведомления)
"""
}


# Функция для клавиатуры главного меню
def main_menu_keyboard() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🌦 Погода", callback_data="help_weather")
    builder.button(text="🧠 ИИ", callback_data="help_ai")
    builder.button(text="📅 Планировщик", callback_data="help_planner")
    builder.adjust(1)  # по одному в строке
    return builder.as_markup()


# Функция для клавиатуры возврата
def back_keyboard() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅ Назад", callback_data="help_back")
    return builder.as_markup()


# Обработчик команды /help
@help_router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        HELP_MAIN_TEXT,
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML"
    )


# Обработчики inline-кнопок
@help_router.callback_query(lambda c: c.data.startswith("help_"))
async def process_help_callback(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]

    if action == "back":
        # Вернуть в главное меню
        await callback.message.edit_text(
            HELP_MAIN_TEXT,
            reply_markup=main_menu_keyboard(),
            parse_mode="HTML"
        )
    else:
        # Показать описание выбранной функции
        text = HELP_DETAILS.get(action, "❌ Описание пока недоступно.")
        await callback.message.edit_text(
            text,
            reply_markup=back_keyboard(),
            parse_mode="HTML"
        )

    await callback.answer()  # закрывает "часики" на кнопке
