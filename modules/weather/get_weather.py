"""
Код для получения погодных данных по API OpenWeather. Возвращает только сырые данные.
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any
import logging


# Логгер для модуля
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeatherService:
    
    def __init__(self, api_key: str, base_url: str = "https://api.openweathermap.org/data/2.5"):
        """
        Инициализация сервиса 
        
        :param API_KEY: API ключ для OpenWeather
        :param base_url: Базовый URL для API
        """

        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.session: Optional[aiohttp.ClientSession] = None # Инициализация сессии будет отложена до первого запроса

    async def __aenter__(self):
        # Инициализация сессии при входе в контекст
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        # Закрытие сессии при выходе из контекста
        await self.close()

    async def _fetch(self, endpoint: str, params: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """
        Вспомогательный метод для выполнения GET-запросов к API.
        :param endpoint: Конечная точка API (например, "weather", "forecast").
        :param params: Параметры запроса.
        :return: Ответ API в виде словаря или None в случае ошибки.
        """
        
        if not self.session:
            self.session = aiohttp.ClientSession()

        params["appid"] = self.api_key

        try:
            async with self.session.get(f"{self.base_url}/{endpoint}", params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_message = await response.text()
                    logger.error(f"Ошибка API: {response.status}: {error_message}")
                    return None
                
        except asyncio.TimeoutError:
            logger.error("⏱ Таймаут при запросе к OpenWeather")
        except aiohttp.ClientError as e:
            logger.error(f"🌐 Ошибка клиента: {e}")
        except Exception as e:
            logger.error(f"❌ Неизвестная ошибка: {e}")

        return None
    
    # ================= Методы для получения различных типов погодных данных ================= #
         

    async def get_current_weather(self,
                                  lat: float,
                                  lon: float,
                                  units: str = "metric",
                                  lang: str = "ru") -> Optional[Dict[str, Any]]:
        """
        Получение текущей погоды по координатам.

        Args:
            lat (float): Широта.
            lon (float): Долгота.
            units (str, optional): Единицы измерения. По умолчанию "metric".
            lang (str, optional): Язык ответа. По умолчанию "ru".

        Returns:
            Optional[Dict[str, Any]]: Словарь с данными о погоде или None в случае ошибки.
        """

        # Вадидация координат
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            logger.error("Некорректные координаты.")
            return None
        
        # Параметры для API-запроса
        params = {
            "lat": lat,
            "lon": lon,
            "units": units,
            "lang": lang
        }

        return await self._fetch("weather", params)

    async def get_forecast(self,
                                   lat: float,
                                   lon: float,
                                   units: str = "metric",
                                   lang: str = "ru") -> Optional[Dict[str, Any]]:
        """
        Получение прогноза погоды на 5 дней с шагом 3 часа по координатам.
        Args:
            lat (float): Широта.
            lon (float): Долгота.
            units (str, optional): Единицы измерения. По умолчанию "metric".
        Returns:
            Optional[Dict[str, Any]]: Словарь с данными о прогнозе погоды или None в случае ошибки.
        """

        # Вадидация координат
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            logger.error("Некорректные координаты.")
            return None
        
        params = {
            "lat": lat,
            "lon": lon,
            "units": units,
            "lang": lang
        }

        return await self._fetch("forecast", params)
    
        
    async def close(self):
        """
        Закрытие сессии.
        """
        if self.session:
            await self.session.close()
            self.session = None