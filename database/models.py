from sqlalchemy import Column , ForeignKey, Integer, String, Float, DateTime, Date

from sqlalchemy.orm import relationship
from .database import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    weathers = relationship("Weather", back_populates="city", lazy="dynamic")


class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True)
    temp = Column(Float)
    temp_fahr = Column(Float)

    owner_city = Column(Integer, ForeignKey("cities.id"))

    city = relationship("City", back_populates="weathers")

class Forecast(Base):
    __tablename__ = "forecasts"

    id = Column(Integer, primary_key=True, index=True)
    date= Column(Date, index=True)
    temp_day = Column(Float)
    temp_fahr_day = Column(Float)
    
    owner_city = Column(Integer, ForeignKey("cities.id"))

class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    date= Column(DateTime, index=True)
    temp= Column(Float)
    temp_fahr = Column(Float)
    
    owner_city = Column(Integer, ForeignKey("cities.id"))
