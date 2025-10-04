# file: reverse_geocode_openweather_async.py
import asyncio
import aiohttp
from typing import Optional, Dict
from config import OPENWEATHER_API_KEY

from pprint import pprint


"""
Асинхронно получает информацию о местоположении по географическим координатам через OpenWeather API.
    
Args:
lat (float): Широта места
lon (float): Долгота места  
api_key (str, optional): Ключ API OpenWeather. Если не указан, берется из config.py
limit (int, optional): Максимальное количество возвращаемых результатов. По умолчанию 1.
        
Returns:
Optional[Dict]: Словарь с данными о местоположении или None в случае ошибки.
Структура ответа:
    {
        "name": "Основное название города (обычно на английском)",
        "local_names": "Словарь с названиями на разных языках(ru, en)",
        "state": "Регион/область/штат", 
        "country": "Код страны (2 символа)",
        "lat": "Широта",
        "lon": "Долгота"
    }
        
Raises:
ValueError: Если API ключ не задан ни в параметрах, ни в config.py
"""
URL = "http://api.openweathermap.org/geo/1.0/reverse"


async def get_location_from_coords_async(lat: float, lon: float, api_key: Optional[str] = None, limit: int = 1) -> Optional[Dict]:
    key = api_key or OPENWEATHER_API_KEY
    if not key:
        raise ValueError("API key не задан. Установи OPENWEATHER_API_KEY в окружении или передай api_key в функцию.")

    # параметры для API-запроса
    params = {
        "lat": str(lat),
        "lon": str(lon),
        "limit": str(limit),
        "appid": key
    }

    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.get(URL, params=params) as resp:
                # если статус запроса != ОК
                if resp.status != 200:
                    text = await resp.text()
                    # вывод ошибки в терминал
                    print(f"HTTP {resp.status}: {text}")
                    return None
                
                data = await resp.json()

                # если API вернул пустой jsom-файл 
                if not data:
                    return None
                place = data[0]

                local_names = place.get("local_names", {})

                # возвращаем все нужные данные
                return {
                    "name": place.get("name"),
                    "ru_name": local_names.get("ru", place.get("name")),
                    "en_name": local_names.get("en", place.get("name")),
                    # "ba_name": local_names.get("ba", place.get("name")),
                    "state": place.get("state"),
                    "country": place.get("country"),
                    "lat": place.get("lat"),
                    "lon": place.get("lon")
                }
            
        except asyncio.TimeoutError:
            print("Timeout при запросе к OpenWeather.")
        except aiohttp.ClientError as e:
            print(f"Network/Client error: {e}")
    return None

