def format_weather(data: dict) -> str:
    if data.get("cod") != 200:
        return "❌ Город не найден."

    city = data["name"]
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    description = data["weather"][0]["description"].capitalize()

    return (
        f"📍 Погода в {city}:\n"
        f"🌡 Температура: {temp}°C (ощущается как {feels_like}°C)\n"
        f"☁ {description}"
    )
