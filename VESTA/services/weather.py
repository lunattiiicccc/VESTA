
import requests


# -----------------------------------------
# DEFAULT LOCATION
# -----------------------------------------

DEFAULT_LOCATION = "Huddersfield"

LOCATIONS = {
    "Huddersfield": {
        "latitude": 53.6458,
        "longitude": -1.7850,
    },
}


# -----------------------------------------
# OPEN-METEO SETTINGS
# -----------------------------------------

WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODES = {
    0: ("Sunny", "Clear sky"),
    1: ("Sunny", "Mainly clear"),
    2: ("Cloudy", "Partly cloudy"),
    3: ("Cloudy", "Overcast"),
    45: ("Cloudy", "Fog"),
    48: ("Cloudy", "Depositing rime fog"),
    51: ("Rainy", "Light drizzle"),
    53: ("Rainy", "Moderate drizzle"),
    55: ("Rainy", "Dense drizzle"),
    56: ("Rainy", "Freezing drizzle"),
    57: ("Rainy", "Dense freezing drizzle"),
    61: ("Rainy", "Slight rain"),
    63: ("Rainy", "Moderate rain"),
    65: ("Rainy", "Heavy rain"),
    66: ("Rainy", "Freezing rain"),
    67: ("Rainy", "Heavy freezing rain"),
    71: ("Snowy", "Slight snowfall"),
    73: ("Snowy", "Moderate snowfall"),
    75: ("Snowy", "Heavy snowfall"),
    77: ("Snowy", "Snow grains"),
    80: ("Rainy", "Slight rain showers"),
    81: ("Rainy", "Moderate rain showers"),
    82: ("Rainy", "Violent rain showers"),
    85: ("Snowy", "Slight snow showers"),
    86: ("Snowy", "Heavy snow showers"),
    95: ("Rainy", "Thunderstorm"),
    96: ("Rainy", "Thunderstorm with hail"),
    99: ("Rainy", "Heavy thunderstorm with hail"),
}


# -----------------------------------------
# WEATHER CLASSIFICATION
# -----------------------------------------

def classify_weather(weather_code, wind_speed):
    """Convert Open-Meteo weather codes into VESTA conditions."""

    weather, description = WEATHER_CODES.get(
        weather_code,
        ("Cloudy", "Unknown conditions"),
    )

    # Strong wind can be useful as a separate styling condition.
    if wind_speed is not None and wind_speed >= 30:
        if weather in ["Sunny", "Cloudy"]:
            weather = "Windy"

    return weather, description


# -----------------------------------------
# GET CURRENT WEATHER
# -----------------------------------------

def get_current_weather(location=DEFAULT_LOCATION):
    """
    Retrieve current weather conditions from Open-Meteo.

    Returns a dictionary containing weather information,
    or raises an exception if the request fails.
    """

    if location not in LOCATIONS:
        raise ValueError(f"Location not supported: {location}")

    coordinates = LOCATIONS[location]

    parameters = {
        "latitude": coordinates["latitude"],
        "longitude": coordinates["longitude"],
        "current": (
            "temperature_2m,"
            "weather_code,"
            "wind_speed_10m,"
            "precipitation"
        ),
        "timezone": "Europe/London",
    }

    response = requests.get(
        WEATHER_API_URL,
        params=parameters,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    if "current" not in data:
        raise ValueError("Weather information was not returned.")

    current = data["current"]

    temperature = current.get("temperature_2m")
    weather_code = current.get("weather_code")
    wind_speed = current.get("wind_speed_10m")
    precipitation = current.get("precipitation")

    if temperature is None or weather_code is None:
        raise ValueError("Incomplete weather information received.")

    weather, description = classify_weather(
        weather_code,
        wind_speed,
    )

    return {
        "location": location,
        "temperature": round(temperature, 1),
        "weather": weather,
        "description": description,
        "wind_speed": wind_speed,
        "precipitation": precipitation,
        "time": current.get("time"),
    }
