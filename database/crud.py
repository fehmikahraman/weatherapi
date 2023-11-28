from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime, date, timedelta
from config import  time_to_update_current_weather
from fastapi import HTTPException



def create_city(db: Session, city: str):
    db_city = models.City(name=city)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session, skip: int = 0, limit: int = 10):
     return db.query(models.City).offset(skip).limit(limit).all()


def check_city_db(db: Session, city: str):
    mycity = db.query(models.City).filter(models.City.name == city).first()
    if not mycity:
        raise HTTPException(status_code = 500, detail = "Please just request supported cities")
    return mycity


def create_weather(db: Session, weather:schemas.WeatherIn):
    db_weather = models.Weather(**weather.model_dump() )
    db.add(db_weather)
    db.commit()
    db.refresh(db_weather)
    return db_weather



def get_weather_today(db:Session, city:schemas.City, date: datetime):
    prev_hour = date - timedelta(minutes=time_to_update_current_weather)
    return db.query(models.Weather).filter(models.Weather.date > prev_hour, 
                                           models.Weather.owner_city==city.id).first()

def check_forecast_db(db : Session, city: schemas.City, nextdays:int, date:date):
    max_date = date + timedelta(nextdays-1)
    return db.query(models.Forecast).filter(models.Forecast.date.between(date,max_date), 
                                            models.Forecast.owner_city==city.id).all()

def create_forecast(db: Session, forecasts: schemas.ForecastIn):
    for forecast in forecasts:
        db_forecast = models.Forecast(**forecast.model_dump())
        record= db.query(models.Forecast).filter(models.Forecast.date==db_forecast.date,
                                            models.Forecast.owner_city==db_forecast.owner_city).first()
        if not record:
            db.add(db_forecast)
    db.commit()
    return forecasts

def check_history_db(db : Session, city: schemas.City, prev:int, date:date):
    min_date = date - timedelta(prev)
    return db.query(models.History).filter(models.History.date.between(min_date,date), 
                                            models.History.owner_city==city.id).all()


def create_history(db: Session, history_data: schemas.HistoryIn):
    for history in history_data:
        db_history = models.History(**history.model_dump())
        record= db.query(models.History).filter(models.History.date==db_history.date,
                                            models.History.owner_city==db_history.owner_city).first()
        if not record:
            db.add(db_history)
    db.commit()
    return history_data