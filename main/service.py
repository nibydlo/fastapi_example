from datetime import datetime, timedelta
from scipy import spatial
from typing import List

from dbservice import DatabaseService
from utils import get_random_vec
from weather import is_weather_comfortable

N_RECOMMENDATIONS = 5
N_CANDIDATES = 10


class Service():
    def __init__(self):
        self.db_service = DatabaseService()
        self.db_service.init_users_table()
        self.db_service.add_user(111, get_random_vec())
        self.db_service.init_places_table()
        self.db_service.fill_places_table()
        self.cache = {}  # uid -> (timestamp, [place_id])

    def get_recommendation_for_uid_by_city_and_type(self, uid: int, city: str, indoor_only: bool = False) -> List:
        user_vec = self.db_service.get_user_vector(uid)
        if not user_vec:
            return []

        random_places = self.db_service.get_random_places(n_places=N_CANDIDATES, city=city, indoor_only=indoor_only)
        if not random_places:
            return []

        places_vectors = [list(place[-50:]) for place in random_places]
        places_tree = spatial.KDTree(places_vectors)

        D, I = places_tree.query(user_vec, N_RECOMMENDATIONS)
        recs = [random_places[i][0] for i in I]
        return recs

    def get_recommendation_for_uid(self, uid: int, city: str, day_from_now: int):
        if uid in self.cache and datetime.now() - self.cache[uid][0] < timedelta(days=1) and self.cache[uid][1]:
            return self.cache[uid][1]

        indoor_only = not is_weather_comfortable(city, day_from_now)
        recs = self.get_recommendation_for_uid_by_city_and_type(uid, city, indoor_only)
        self.cache[uid] = (datetime.now(), recs)
        return recs
