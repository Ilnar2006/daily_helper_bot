import json
import os
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from services.get_geo import get_location_from_coords_async
from .start_keyboard import gender_keyboard, social_status_keyboard, confirm_keyboard, main_menu_keyboard, send_location_keyboard

start_router = Router()

JSON_FILE_PATH = "data/users.json"


# Машина состояний для регистрации пользователя 
class Registration(StatesGroup):
    name = State()
    gender = State()
    age = State()
    status = State()
    city = State()
    location = State()
    confirm = State()


# работа с JSON-файлом (загрузка и сохранение)
def load_users():
    if not os.path.exists(JSON_FILE_PATH):
        return {}
    with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users):
    with open(JSON_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)


# =================================
# Хендлеры
# =================================

# Старт
@start_router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    users = load_users()
    user_id = str(message.from_user.id)

    # Если пользователь уже есть в базе, приветствуем его и показываем главное меню
    if user_id in users:
        await message.answer(
            """👋 С возвращением!
            Я — твой персональный ассистент.
            Помогаю следить за задачами, подсказывать погоду, 
            и у меня есть встроенный AI.
            Выбери действие:""",
            reply_markup=main_menu_keyboard()
        )

    # Иначе начинаем регистрацию
    else:
        await message.answer("Привет 👋 Вижу ты тут впервые. Давай познакомимся! Как тебя зовут?")
        await state.set_state(Registration.name)


# Имя пользователя 
@start_router.message(Registration.name)
async def reg_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer("Отлично! 🚀 Укажи свой пол:", reply_markup=gender_keyboard())
    await state.set_state(Registration.gender)


# Пол 
@start_router.callback_query(Registration.gender, F.data.startswith("gender_"))
async def reg_gender(callback: CallbackQuery, state: FSMContext):
    gender = "Мужской" if callback.data == "gender_m" else "Женский"
    await state.update_data(gender=gender)

    await callback.message.answer("Теперь введи свой возраст:")
    await state.set_state(Registration.age)
    await callback.answer()


# Возраст
@start_router.message(Registration.age)
async def reg_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)

    await message.answer("Какой у тебя социальный статус?", 
                         reply_markup=social_status_keyboard())
    await state.set_state(Registration.status)


# Соц. статус
@start_router.callback_query(Registration.status)
async def reg_status(callback: CallbackQuery, state: FSMContext):
    status_map = {
        "social_status_schoolboy": "Школьник",
        "social_status_student": "Студент",
        "social_status_worker": "Рабочий",
        "social_status_other": "Другое"
    }

    status = status_map.get(callback.data, "Неизвестно")
    await state.update_data(status=status)

    # Объясняем, что можно сделать — отправить локацию (кнопка) или просто написать город
    await callback.message.answer(
        "🌍 Укажи, пожалуйста, город проживания.\n"
        "— Нажми кнопку «Отправить геолокацию», если хочешь автоматически определить город (работает на мобильных).\n"
        "— Или просто напиши город текстом.",
        reply_markup=send_location_keyboard)  # это ReplyKeyboardMarkup с request_location=True
    # важно: убрать спиннер у нажатой inline-кнопки
    await callback.answer()
    # ставим состояние ожидания ввода города
    await state.set_state(Registration.city)


# ---- Универсальный обработчик для состояния Registration.city ----
@start_router.message(Registration.city)
async def reg_city(message: types.Message, state: FSMContext):
    """
    Обрабатываем либо присланную локацию (message.location),
    либо текст (message.text).
    Если ничего подходящего — просим повторить.
    """
    # 1) Пользователь прислал геолокацию (работает на мобильных)
    if message.location is not None:
        lat = message.location.latitude
        lon = message.location.longitude

        # (Опционально) reverse geocoding: определить название города по координатам.
        try:
            user_location = await get_location_from_coords_async(lat, lon) # данные о местоположении пользователя - словарь {"name", "ru_name", "en_name", "state", "country", "lat", "lon"}
            
            if user_location and user_location.get("ru_name"):

                city = user_location["ru_name"]  # название города на русском
                await state.update_data(city=city, location={"lat": lat, "lon": lon})

                await message.answer(
                    f"Отлично, определил ваш город {city}", reply_markup=ReplyKeyboardRemove()
                    )
                
            else:
                await message.answer("Не удалось определить город по координатам. Пожалуйста, попробуйте заново отправить локацию. Если ничего не помогает, то вы сможете настроить город позже", reply_markup=send_location_keyboard())

                return  # остаёмся в том же состоянии — ждём корректного ввода
            
        except Exception as e:
            print(f"Error in geocoding: {e}")
            # даём понятную подсказку и оставляем состояние Registration.city
            await message.answer(
                "⚠️ Ошибка при определении местоположения. "
                "Вы можете пропустить этот шаг.",
                reply_markup=send_location_keyboard()
                )
            return  # остаёмся в том же состоянии — ждём корректного ввода


    # 2) Пользователь нажал кнопку "Пропустить" 
    elif message.text and message.text.strip() == "➡️ Пропустить":
        await state.update_data(city=None, location={"lat": None, "lon": None})

        # убрать reply-клавиатуру (на случай, если она осталась)
        await message.answer("Вы пропустили указание города. Вы всегда можете настроит его через команду /settings", reply_markup=ReplyKeyboardRemove())

    # 3) Что-то непонятное пришло (пользователь нажал кнопку на Desktop, но локация не отправилась)
    else:
        # даём понятную подсказку и оставляем состояние Registration.city
        await message.answer(
            "Пожалуйста, используйте кнопки ниже:\n\n"
            "• 📍 **Отправить местоположение** - для автоматического определения города\n"
            "• ➡️ **Пропустить** - если не хотите указывать сейчас\n\n"
            "Вы всегда сможете изменить настройки позже.",
            reply_markup=send_location_keyboard()
        )
        return  # остаёмся в том же состоянии — ждём корректного ввода

     # После успешного получения city — показываем итог и просим подтверждение
    data = await state.get_data() # сохраняем данные из class Registration в переменную data
    # формируем текст с данными для подтверждения 
    text = ( # многострочный f-string с данными из state data 
        f"📋 Проверь данные:\n\n"
        f"Имя: {data.get('name') or "❌ Не определено"}\n"
        f"Пол: {data.get('gender') or "❌ Не определено"}\n"
        f"Возраст: {data.get('age') or "❌ Не определено"}\n"
        f"Статус: {data.get('status') or "❌ Не определено"}\n"
        f"Город: {data.get('city') or "❌ Не определено"}\n\n"
        "Всё верно? Если нет, то ты можешь заново пройти регистрацию."
    )

    await message.answer(text, reply_markup=confirm_keyboard())  # inline-кнопки "Да / Изменить"
    await state.set_state(Registration.confirm)


# Подтверждение — ДА
@start_router.callback_query(Registration.confirm, F.data == "confirm_yes")
async def reg_confirm_yes(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    users = load_users()
    user_id = str(callback.from_user.id)

    users[user_id] = {
        "id": callback.from_user.id,
        "name": data.get("name", ""),
        "age": int(data.get("age", 0)),
        "gender": data.get("gender", ""),
        "city": data.get("city", ""),
        "location": data.get("location", {}),  # здесь словарь с lat/lon/ru_name
        "status": data.get("status", ""),
        "preferences": {
            "notifications": True,
            "language": "ru",
            "timezone": ""
        }
    }
    save_users(users)

    await callback.message.answer("✅ Отлично! Ты зарегистрирован!")
    await callback.message.answer(
        "Теперь доступно главное меню 👇",
        reply_markup=main_menu_keyboard()
    )
    await state.clear()
    await callback.answer()


# Подтверждение — Редактировать
@start_router.callback_query(Registration.confirm, F.data == "confirm_edit")
async def reg_confirm_edit(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("✏ Окей, давай начнём заново. Введи своё имя:")
    await state.set_state(Registration.name)
    await callback.answer()
