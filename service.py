from datetime import date
from enum import Enum
from typing import List


def get_suggestions_for_uid(uid: int) -> List[int]:
    recommendations_for_uid = {
        1: [1, 2, 3, 4],
        2: [2, 5, 6, 9],
        3: [4, 7, 8]
    }

    return recommendations_for_uid[uid] if uid in recommendations_for_uid else []


def get_visited_for_uid(uid: int) -> List[int]:
    visited_for_uids = {
        1: [3, 4],
        2: [2],
        3: [5]
    }
    return visited_for_uids[uid] if uid in visited_for_uids else []


class Weather(Enum):
    SUN = 1
    RAIN = 2


def get_weather_for_date(date_for_search: date) -> Weather:
    if date_for_search.day % 2:
        return Weather.SUN
    else:
        return Weather.RAIN


class PlaceType(Enum):
    INDOOR = 1
    OUTDOOR = 2


def get_place_type(place_id: int) -> PlaceType:
    if place_id % 2:
        return PlaceType.INDOOR
    else:
        return PlaceType.OUTDOOR


def filter_visited_places(places: List[int], uid: int) -> List[int]:
    visited = get_visited_for_uid(uid)
    places_set = set(places)
    places_set.difference_update(visited)
    return list(places_set)


def is_place_suitable_for_weather(place_id: int, weather: Weather) -> bool:
    place_type = get_place_type(place_id)
    return place_type == PlaceType.INDOOR or place_type == PlaceType.OUTDOOR and weather == Weather.SUN


def filter_places_by_weather(places: List[int], date_for_search: date) -> List[int]:
    weather = get_weather_for_date(date_for_search)
    return [place_id for place_id in places if is_place_suitable_for_weather(place_id, weather)]


def get_recommendation_for_uid(uid: int, date_for_search: date) -> List[int]:
    recommendations = get_suggestions_for_uid(uid)
    not_visited = filter_visited_places(recommendations, uid)
    recommended_places = filter_places_by_weather(not_visited, date_for_search)
    return recommended_places
