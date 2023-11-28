from pydantic import BaseModel
from datetime import datetime, date


class WeatherIn(BaseModel):
    date: datetime
    temp: float
    temp_fahr : float
    owner_city: int

class Weather(WeatherIn):
    id: int
    class Config:
        orm_mode = True

class CityIn(BaseModel):
    name: str


class City(CityIn):
    id: int
    weathers: list[Weather] = []
    class Config:
        orm_mode = True

class ForecastIn(BaseModel):
    date:date
    temp_day: float
    temp_fahr_day: float
    owner_city: int

class Forecast(ForecastIn):
    id: int
    class Config:
        orm_mode = True


class HistoryIn(BaseModel):
    date:datetime
    temp: float
    temp_fahr: float
    owner_city: int

class History(HistoryIn):
    id: int
    class Config:
        orm_mode = True