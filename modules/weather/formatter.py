async def format_current_weather(data: dict) -> str:
    """
    Форматирует данные о текущей погоде для удобного отображения.

    Args:
        data (dict): Словарь с данными о погоде.

    Returns:
        str: Отформатированная строка с информацией о погоде.
    """
    if not data:
        return "Нет данных о погоде."

    weather = data.get("weather", [{}])[0]
    main = data.get("main", {})
    wind = data.get("wind", {})

    description = weather.get("description", "Нет описания")
    temperature = main.get("temp", 0)
    feels_like = main.get("feels_like", 0)
    humidity = main.get("humidity", 0)
    wind_speed = wind.get("speed", 0)

    return (f"🌤️ Погода: {description}\n"
            f"🌡️ Температура: {temperature}°C\n"
            f"💨 Ощущается как: {feels_like}°C\n"
            f"💧 Влажность: {humidity}%\n"
            f"🌬️ Скорость ветра: {wind_speed} м/с\n"
            f"📍 Москва, Россия")

async def format_forecast(data: dict) -> str:
    """
    Форматирует данные о прогнозе погоды для удобного отображения.

    Args:
        data (dict): Словарь с данными о прогнозе погоды.

    Returns:
        str: Отформатированная строка с информацией о прогнозе погоды.
    """
    if not data or "list" not in data:
        return "Нет данных о прогнозе погоды."

    forecast_lines = []
    for entry in data["list"]:
        dt_txt = entry.get("dt_txt", "Нет времени")
        weather = entry.get("weather", [{}])[0]
        main = entry.get("main", {})
        wind = entry.get("wind", {})

        description = weather.get("description", "Нет описания")
        temperature = main.get("temp", 0)
        humidity = main.get("humidity", 0)
        wind_speed = wind.get("speed", 0)

        forecast_lines.append(
            (f"📅 {dt_txt}\n"
             f"🌤️ Погода: {description}\n"
             f"🌡️ Температура: {temperature}°C\n"
             f"💧 Влажность: {humidity}%\n"
             f"🌬️ Скорость ветра: {wind_speed} м/с\n")
        )

    return "\n".join(forecast_lines)

async def format_weekly_forecast(data: dict) -> str:
    """
    Форматирует данные о недельном прогнозе погоды для удобного отображения.

    Args:
        data (dict): Словарь с данными о недельном прогнозе погоды.

    Returns:
        str: Отформатированная строка с информацией о недельном прогнозе погоды.
    """
    if not data or "list" not in data:
        return "Нет данных о недельном прогнозе погоды."

    daily_forecast = {}
    for entry in data["list"]:
        date = entry.get("dt_txt", "").split(" ")[0]
        if date not in daily_forecast:
            daily_forecast[date] = []
        daily_forecast[date].append(entry)

    forecast_lines = []
    for date, entries in daily_forecast.items():
        temps = [e.get("main", {}).get("temp", 0) for e in entries]
        descriptions = [e.get("weather", [{}])[0].get("description", "Нет описания") for e in entries]
        avg_temp = sum(temps) / len(temps) if temps else 0
        common_description = max(set(descriptions), key=descriptions.count) if descriptions else "Нет описания"

        forecast_lines.append(
            (f"📅 {date}\n"
             f"🌤️ Погода: {common_description}\n"
             f"🌡️ Средняя температура: {avg_temp:.1f}°C\n")
        )

    return "\n".join(forecast_lines)

async def format_tomorrow_weather(data: dict) -> str:
    """
    Форматирует данные о погоде на завтра для удобного отображения.

    Args:
        data (dict): Словарь с данными о прогнозе погоды.

    Returns:
        str: Отформатированная строка с информацией о погоде на завтра.
    """
    if not data or "list" not in data:
        return "Нет данных о погоде на завтра."

    tomorrow_date = None
    for entry in data["list"]:
        dt_txt = entry.get("dt_txt", "")
        if " " in dt_txt:
            date_part = dt_txt.split(" ")[0]
            if tomorrow_date is None:
                tomorrow_date = date_part
            elif date_part != tomorrow_date:
                break

        weather = entry.get("weather", [{}])[0]
        main = entry.get("main", {})
        wind = entry.get("wind", {})

        description = weather.get("description", "Нет описания")
        temperature = main.get("temp", 0)
        humidity = main.get("humidity", 0)
        wind_speed = wind.get("speed", 0)

        return (f"📅 Погода на завтра ({tomorrow_date}):\n"
                f"🌤️ Погода: {description}\n"
                f"🌡️ Температура: {temperature}°C\n"
                f"💧 Влажность: {humidity}%\n"
                f"🌬️ Скорость ветра: {wind_speed} м/с\n")

    return "Нет данных о погоде на завтра."