import logging

import numpy as np


city_to_coordinates = {
    'spb': {'lat': '59.937500', 'lon': '30.308600'},
    'msk': {'lat': '55.7558', 'lon': '37.6173'}
}
VEC_SIZE = 50


def check_city(city: str) -> bool:
    if city not in city_to_coordinates:
        logging.warning('unsupported city:' + city)
        return False
    return True


def check_day_from_now(day_from_now: int) -> bool:
    if day_from_now > 30:
        logging.warning('support only 30 days from today')
        return False
    return True


def get_random_vec():
    return list(np.random.rand(VEC_SIZE))
