from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database.database import SessionLocal
from database import crud, schemas
from config import max_days_forecast, max_days_history
from datetime import datetime, timedelta, date
from services.openweather import get_weather, get_history, get_forecast
from tools.converters import convertCelsiustoFahrenheit





router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.get("/")
async def read_main():
    return {"message": "Weather API"}


@router.get("/cities")
async def get_cities(db: Session= Depends(get_db)):
    """Returns supported cities."""
    return crud.get_cities(db)

@router.get("/weather/{city}")
async def get_weather_now(city: str, db: Session= Depends(get_db)):
    """Returns a city weather."""
    city_asked= crud.check_city_db(db, city=city)

    weather_asked = crud.get_weather_today(db, city_asked, datetime.today().replace(microsecond = 0))
    if not weather_asked:
        response = await get_weather(city )
        dt = response["dt"]
        response = response["main"]
        new_data = {}
        new_data = {
            "date": datetime.fromtimestamp(dt),
            "temp": response["temp"],
            "temp_fahr": convertCelsiustoFahrenheit(response["temp"]),
            "owner_city": city_asked.id,
            }
        return crud.create_weather(db, schemas.WeatherIn(**new_data))
    return weather_asked
    


@router.get("/forecast/{city}")
async def get_weather_forecast(city: str, nextdays: int,  db: Session= Depends(get_db)):
    """Returns city weather forecasts for the coming days (up to 7 days)."""
    city_asked= crud.check_city_db(db, city=city)
    if nextdays < 1 or nextdays > max_days_forecast:
        raise HTTPException(
            500, detail="API only returns 7 days forecast. Please request forecats with nextdays between 1 and 7."
        )
    forecast_asked =  crud.check_forecast_db(db, city_asked, nextdays, datetime.date(datetime.now()))
    if len(forecast_asked) < nextdays:
        forecast_response = await get_forecast(city, nextdays)
        response = forecast_response["list"]
        new_data = []
        for forecast in response:
            new_data_item ={
            "date": date.fromtimestamp(forecast["dt"]),
            "temp_day": forecast["temp"]["day"],
            "temp_fahr_day": convertCelsiustoFahrenheit(forecast["temp"]["day"]),
            "owner_city": city_asked.id,
            }
            new_data.append(schemas.ForecastIn(**new_data_item))
        return crud.create_forecast(db, new_data)
    return forecast_asked


@router.get("/history/{city}")
async def get_weather_history(city: str, country: str, prev: int,  db: Session= Depends(get_db)):
    """Returns city weather history for the past days (up to 7 days)."""
    city_asked= crud.check_city_db(db, city=city)
    if prev < 1 or prev > max_days_history:
        raise HTTPException(
            500, detail="API only returns 7 days history. Please request forecats with prev between 1 and 7."
        )
    history_asked =  crud.check_history_db(db, city_asked, prev, datetime.today().replace(microsecond = 0))
    if len(history_asked)< (prev*23):
        start = datetime.today() - timedelta(days=prev)
        start = int(start.timestamp())
        end = int(datetime.today().timestamp())
        history_asked = await get_history( city, country, start, end)
        history_asked = history_asked["list"]
        new_data = []
        for history in history_asked:
            new_data_item ={
            "date": datetime.fromtimestamp(history["dt"]),
            "temp": history["main"]["temp"],
            "temp_fahr": convertCelsiustoFahrenheit(history["main"]["temp"]),
            "owner_city": city_asked.id,
            }
            new_data.append(schemas.HistoryIn(**new_data_item))
        return crud.create_history(db, new_data)
    return history_asked
     




