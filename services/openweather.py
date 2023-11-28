import http
import httpx
import os
from fastapi.exceptions import HTTPException
from config import units

from httpx import Response

from dotenv import load_dotenv
# load environment variables from .env file

load_dotenv()

api_key = os.getenv("API_KEY")
api_key_history = os.getenv("API_KEY_HISTORY")


async def get_weather( city: str):
    
    async with httpx.AsyncClient() as client:
        response: Response = await client.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}'
        )
        if http.HTTPStatus(response.status_code) != http.HTTPStatus.OK:
            raise HTTPException(response.status_code, detail=response.text)
        return response.json()


async def get_history(city: str, country: str, start: str, end: str):
    async with httpx.AsyncClient() as client:
        response: Response = await client.get(
            f'https://history.openweathermap.org/data/2.5/history/city?q={city+","+country}&type=hour&appid={api_key_history}&units={units}&start={start}&end={end}&cnt=1'
        )
        if http.HTTPStatus(response.status_code) != http.HTTPStatus.OK:
            raise HTTPException(response.status_code, detail=response.text)
        return response.json()


async def get_forecast(city: str, cnt: int):
    async with httpx.AsyncClient() as client:
        response: Response = await client.get(
            f'https://api.openweathermap.org/data/2.5/forecast/daily?q={city}&appid={api_key}&units={units}&cnt={cnt}'
        )
        if http.HTTPStatus(response.status_code) != http.HTTPStatus.OK:
            raise HTTPException(response.status_code, detail=response.text)
        return response.json()