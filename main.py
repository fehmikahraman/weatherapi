from fastapi import FastAPI
from routers.weather import router as weather_router
from database import models
from database.database import engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(weather_router)

