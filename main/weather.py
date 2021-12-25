import logging
import requests

from utils import city_to_coordinates

API_KEY = 'ac2522b9fc413ba3ad68cb6d0f340c17'
WEATHER_REQUEST_TEMPLATE = "https://api.openweathermap.org/data/2.5/forecast/climate?hourly={api_key}&lat={lat}&lon={lon}"


def get_query(city: str) -> str:
    return WEATHER_REQUEST_TEMPLATE.format(
        api_key=API_KEY,
        lat=city_to_coordinates[city]['lat'],
        lon=city_to_coordinates[city]['lat']
    )


def get_forecast(city: str, day_index: int):
    if day_index >= 30:
        logging.warning('day too far from today, support days closer than 30 from today')
        return False
    query = get_query(city)
    response = requests.get(query).json()
    if response['cod'] != 200:
        logging.warning('api error, code ' + str(response['cod']) + ' message: ' + response['message'])
        return False
    return response['list'][day_index]


def is_weather_comfortable(city: str, day_from_now: int) -> bool:

    forecast = get_forecast(city, day_from_now)
    if not forecast:
        return False

    wind_ok = forecast['wind']['speed'] < 7
    is_sunny = forecast['visibility'] > 1000
    sunny_temp_ok = forecast['feels_like']['day'] > 273 - 20
    not_sunny_temp_ok = forecast['feels_like']['day'] > 273
    return wind_ok and (is_sunny and sunny_temp_ok or not_sunny_temp_ok)
