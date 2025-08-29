import os
import requests
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = "open-weather13.p.rapidapi.com"
BASE_URL = "https://open-weather13.p.rapidapi.com/city"

headers = {"x-rapidapi-key": RAPIDAPI_KEY, "x-rapidapi-host": RAPIDAPI_HOST}


def get_current_weather(city):
    params = {"city": city, "lang": "EN", "units": "metric"}
    response = requests.get(BASE_URL, headers=headers, params=params)
    return response.json()
