import os
import requests
from dotenv import load_dotenv

BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARENT_DIR = os.path.dirname(BASE_DIR)
load_dotenv(os.path.join(BASE_DIR, ".env"))
load_dotenv(os.path.join(PARENT_DIR, ".env"))


def _get_coordinates(city: str) -> tuple:
    """City name → (lat, lon, display_name) using Open-Meteo geocoding (free, no key)."""
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    resp = requests.get(url, timeout=10)
    data = resp.json()
    results = data.get("results", [])
    if not results:
        return None, None, city
    r = results[0]
    name = f"{r.get('name', city)}, {r.get('country', '')}"
    return r["latitude"], r["longitude"], name


def get_weather(location: str) -> dict:
    """Fetch weather using Open-Meteo — 100% free, no API key needed."""
    try:
        lat, lon, display_name = _get_coordinates(location)
        if lat is None:
            return {"error": f"Could not find location: {location}"}

        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,"
            f"wind_speed_10m,weather_code"
            f"&timezone=auto"
        )
        resp = requests.get(url, timeout=10)
        data = resp.json()
        current = data.get("current", {})

        # WMO weather code → description
        wmo = {
            0: "Clear Sky", 1: "Mainly Clear", 2: "Partly Cloudy", 3: "Overcast",
            45: "Foggy", 48: "Icy Fog", 51: "Light Drizzle", 53: "Drizzle",
            55: "Heavy Drizzle", 61: "Light Rain", 63: "Rain", 65: "Heavy Rain",
            71: "Light Snow", 73: "Snow", 75: "Heavy Snow", 80: "Rain Showers",
            81: "Heavy Showers", 82: "Violent Showers", 95: "Thunderstorm",
            96: "Thunderstorm with Hail", 99: "Severe Thunderstorm",
        }
        code = current.get("weather_code", 0)
        condition = wmo.get(code, f"Code {code}")

        return {
            "city":       display_name,
            "temp":       current.get("temperature_2m"),
            "feels_like": current.get("apparent_temperature"),
            "humidity":   current.get("relative_humidity_2m"),
            "condition":  condition,
            "wind_speed": current.get("wind_speed_10m"),
        }
    except Exception as e:
        return {"error": str(e)}


def format_weather(data: dict) -> str:
    if "error" in data:
        return f"Weather Error: {data['error']}"
    return (
        f"🌤 Weather in {data['city']}\n"
        f"  Temperature : {data['temp']}°C (feels like {data['feels_like']}°C)\n"
        f"  Condition   : {data['condition']}\n"
        f"  Humidity    : {data['humidity']}%\n"
        f"  Wind Speed  : {data['wind_speed']} km/h"
    )


def web_search(query: str, max_results: int = 5) -> list:
    return []

def format_search_results(results: list) -> str:
    return ""
