import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(city):
    try:
        base = "http://api.openweathermap.org/data/2.5/weather?"
        url = f"{base}q={city}&appid={API_KEY}&units=metric"
        res = requests.get(url).json()

        if res.get("cod") != 200:
            return f"Min, {city} ka weather nahi mil paaya"

        weather_desc = res["weather"][0]["description"]
        temp = res["main"]["temp"]
        feels = res["main"]["feels_like"]
        humidity = res["main"]["humidity"]

        return f"{city.title()} me mausam {weather_desc} hai, temperature {temp}°C aur humidity {humidity}% hai."

    except Exception as e:
        return f"Min, weather info nahi mil paaya: {e}"