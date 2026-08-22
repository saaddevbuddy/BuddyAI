# ==========================================
# Buddy AI - Weather Module
# ==========================================

import requests


# ==========================================
# Default City
# ==========================================

DEFAULT_CITY = "Mianwali"


# ==========================================
# Get Current Weather
# ==========================================

def get_weather(city=DEFAULT_CITY):

    try:

        if not city:
            city = DEFAULT_CITY

        url = (
            "https://wttr.in/"
            + city
            + "?format=j1"
        )

        response = requests.get(
            url,
            timeout=10
        )

        if response.status_code != 200:
            return None

        data = response.json()

        current = data["current_condition"][0]

        weather = {
            "city": city,
            "temperature": current["temp_C"],
            "feels_like": current["FeelsLikeC"],
            "condition": current["weatherDesc"][0]["value"],
            "humidity": current["humidity"],
            "wind": current["windspeedKmph"]
        }

        return weather

    except Exception as e:

        print("Weather Error:", e)

        return None


# ==========================================
# Format Weather
# ==========================================

def format_weather(weather):

    if not weather:

        return (
            "Sir, weather information "
            "abhi nahi mil saki."
        )

    return (
        f"{weather['city']} ka current weather:\n"
        f"Temperature: {weather['temperature']}°C\n"
        f"Feels Like: {weather['feels_like']}°C\n"
        f"Condition: {weather['condition']}\n"
        f"Humidity: {weather['humidity']}%\n"
        f"Wind: {weather['wind']} km/h"
    )


# ==========================================
# Easy Weather Function
# ==========================================

def ask_weather(city=DEFAULT_CITY):

    weather = get_weather(city)

    return format_weather(weather)