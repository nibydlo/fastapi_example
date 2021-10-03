import pytest

from service import *


def test_get_suggestions_for_existing_user():
    uid = 1
    suggestions = get_suggestions_for_uid(uid)
    expected = [1, 2, 3, 4]
    assert suggestions == expected


def test_get_suggestions_for_non_existing_user():
    uid = 4
    suggestions = get_suggestions_for_uid(uid)
    expected = []
    assert suggestions == expected


def test_get_weather():
    date_for_search = date(2021, 10, 3)
    weather = get_weather_for_date(date_for_search)
    expected = Weather.SUN
    assert weather == expected


def test_filter_visited():
    # интегрирует получение посещенных мест и фильтрацию
    places = [1, 2, 3, 4]
    uid = 1
    not_visited = filter_visited_places(places, uid)
    expected = [1, 2]
    assert not_visited == expected


def test_filter_places_by_weather():
    # интегрирует получение погоды, предикат фильтрации по погоде и саму фильтрацию
    places = [1, 2, 3, 4]
    date_for_search = date(2021, 10, 2)
    filtered_places = filter_places_by_weather(places, date_for_search)
    # weather должна быть SUN, значит подходят только INDOOR места: 1 и 3
    expected = [1, 3]
    assert filtered_places == expected


def test_recommendations():
    # интегрирует весь функционал
    uid = 1
    date_for_search = date(2021, 10, 2)
    recommendations = get_recommendation_for_uid(uid, date_for_search)
    expected = [1]
    assert recommendations == expected
