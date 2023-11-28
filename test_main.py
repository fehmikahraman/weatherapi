from fastapi.testclient import TestClient
from main import app

client= TestClient(app)


def test_get_cities():
    response = client.get("/cities")
    assert response.status_code == 200

def test_get_weather_today():
    response = client.get("/weather/Istanbul")
    assert response.status_code == 200

def test_forecast():
    response = client.get("/forecast/Paris?nextdays=3")
    assert response.status_code == 200

def test_history():
    response = client.get("/history/Istanbul?country=tr&prev=2")
    assert response.status_code == 200

def test_max_days_fail():
    reponse = client.get("/forecast/Paris?nextdays=8")
    assert reponse.status_code == 500

def test_city_fail():
    reponse = client.get("/weather/bursa")
    assert reponse.status_code == 500