# weatherapi

### Installation for Docker

> git clone https://github.com/fehmikahraman/weatherapi.git <br>
> cd weatherapi <br>

Please create .env and include  "API_KEY", "API_KEY_HISTORY" before running. <br>

> docker compose up

## Endpoints (Docker)

>Interactive API document
> http://localhost:4444/docs


> http://localhost:4444/cities


> http://localhost:4444/weather/Istanbul


> http://localhost:4444/forecast/Paris?nextdays=3


> http://localhost:4444/history/Istanbul?country=TR&prev=2


## Run tests

> docker exec weatherapi-web-1 python -m pytest -v



### Installation
> git clone https://github.com/fehmikahraman/weatherapi.git <br>
> cd weatherapi <br>
> pip install -r requirements.txt <br>
> pip install -r requirements-dev.txt <br>

### Run
Please create .env and include  "API_KEY", "API_KEY_HISTORY" before running. 
> uvicorn main:app --reload

### Check it

You can check the interactive API document. Open your browser at http://127.0.0.1:8000/docs  <br>
You can check the API paths and parameters.