import random
from typing import Optional, Tuple, List

import numpy as np
import sqlite3

INIT_PLACES_SCRIPT_TEMPLATE = """
DROP TABLE IF EXISTS places;

CREATE TABLE places (
	place_id INT PRIMARY KEY,
	name VARCHAR(200) NOT NULL,
	city VARCHAR(50) NOT NULL,
	indoor INTEGER NOT NULL,
	rating REAL NOT NULL,
	{}
);
"""

INIT_USERS_SCRIPT_TEMPLATE = """
DROP TABLE IF EXISTS users;

CREATE TABLE users (user_id INT PRIMARY KEY,{});
"""

VEC_SIZE = 50
ADD_PLACE_QUERY_TEMPLATE = \
    """INSERT INTO places (place_id, name, city, indoor, rating, {}) VALUES (?, ?, ?, ?, ?, {})"""
ADD_USER_QUERY_TEMPLATE = """INSERT INTO users (user_id, {}) VALUES (?, {})"""

GET_ALL_PLACES_QUERY = """SELECT * FROM places"""
GET_PLACE_QUERY_TEMPLATE = """SELECT * FROM places WHERE place_id = ?"""
GET_PLACES_BY_CITY_QUERY_TEMPLATE = """SELECT * FROM places WHERE city = ?"""
GET_PLACES_BY_CITY_AND_TYPE_TEMPLATE = """SELECT * FROM places WHERE city = ? AND indoor = ?"""
GET_N_PLACES_BY_CITY_QUERY_TEMPLATE = """SELECT * FROM places WHERE city = ? ORDER BY RANDOM() LIMIT ?"""
GET_N_PLACES_BY_CITY_AND_TYPE_QUERY_TEMPLATE = \
    """SELECT * FROM places WHERE city = ? AND indoor = ? ORDER BY RANDOM() LIMIT ?"""

GET_ALL_USERS_QUERY = """SELECT * FROM users"""
GET_USER_QUERY_TEMPLATE = """SELECT * FROM users WHERE user_id = ?"""

DELETE_PLACE_QUERY_TEMPLATE = """DELETE FROM places WHERE place_id = ?"""
DELETE_USER_QUERY_TEMPLATE = """DELETE FROM users WHERE user_id = ?"""

DELETE_TEST_QUERY_TEMPLATE = """DELETE FROM places WHERE is_test = TRUE"""
DEFAULT_PATH = '.\\db.sqlite'

N_SAMPLE_PLACES = 100

# indoor_place_types = [
#     'cafe',
#     'restaurant',
#     'theatre',
#     'museum'
# ]
#
# outdoor_place_types = [
#     'park',
#     'architecture',
#     'monument',
#     'viewpoint'
# ]


class UnknownUserException(Exception):
    pass


def get_init_places_table_script():
    return INIT_PLACES_SCRIPT_TEMPLATE.format(','.join([' vec_{} REAL NOT NULL'.format(i) for i in range(VEC_SIZE)]))


def get_init_users_table_script():
    return INIT_USERS_SCRIPT_TEMPLATE.format(','.join([' vec_{} REAL NOT NULL'.format(i) for i in range(VEC_SIZE)]))


class DatabaseService():
    def __init__(self, path: str = DEFAULT_PATH):
        self.path = path
        self.connection = self.create_connection()

    @staticmethod
    def get_add_user_query_template():
        return ADD_USER_QUERY_TEMPLATE.format(
            ','.join(['vec_{}'.format(i) for i in range(VEC_SIZE)]),
            ','.join(['?' for _ in range(VEC_SIZE)])
        )

    @staticmethod
    def get_add_place_query_template():
        return ADD_PLACE_QUERY_TEMPLATE.format(
            ','.join(['vec_{}'.format(i) for i in range(VEC_SIZE)]),
            ','.join(['?' for _ in range(VEC_SIZE)])
        )

    def create_connection(self) -> Optional[sqlite3.Connection]:
        try:
            connection = sqlite3.connect(self.path, check_same_thread=False)
            return connection
        except sqlite3.Error as e:
            print(f'Error while creating db connection: {e}')

    def close_connection(self):
        self.connection.close()

    def init_places_table(self):
        cursor = self.connection.cursor()
        cursor.executescript(get_init_places_table_script())
        self.connection.commit()
        cursor.close()

    def init_users_table(self):
        cursor = self.connection.cursor()
        cursor.executescript(get_init_users_table_script())
        self.connection.commit()
        cursor.close()

    def __run_query_void(self, query_template: str, args: Tuple):
        cursor = self.connection.cursor()
        cursor.execute(query_template, args)
        self.connection.commit()
        cursor.close()

    def add_place(self, place_id: int, name: str, city: str, indoor: bool, rating: float, vec: List[float]):
        # print(place_id, name, city, int(indoor), rating, vec)
        self.__run_query_void(self.get_add_place_query_template(), (place_id, name, city, int(indoor), rating, *vec))

    def add_user(self, user_id: int, vec: List[float]):
        self.__run_query_void(self.get_add_user_query_template(), (user_id, *vec))

    def delete_place(self, place_id: int):
        self.__run_query_void(DELETE_PLACE_QUERY_TEMPLATE, (place_id,))

    def delete_user(self, user_id: int):
        self.__run_query_void(DELETE_USER_QUERY_TEMPLATE, (user_id,))

    def delete_test(self):
        self.__run_query_void(DELETE_TEST_QUERY_TEMPLATE, ())

    def get_all_places(self) -> list:
        cursor = self.connection.cursor()
        cursor.execute(GET_ALL_PLACES_QUERY)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def get_place(self, place_id: int):
        cursor = self.connection.cursor()
        cursor.execute(GET_PLACE_QUERY_TEMPLATE, (place_id,))
        row = cursor.fetchone()
        cursor.close()
        return row

    def get_places_by_city(self, region_id: int) -> list:
        cursor = self.connection.cursor()
        cursor.execute(GET_PLACES_BY_CITY_QUERY_TEMPLATE, (region_id,))
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def get_all_users(self):
        cursor = self.connection.cursor()
        cursor.execute(GET_ALL_USERS_QUERY)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def get_user(self, user_id: int):
        cursor = self.connection.cursor()
        cursor.execute(GET_USER_QUERY_TEMPLATE, (user_id,))
        row = cursor.fetchone()
        cursor.close()
        return row

    def get_user_vector(self, uid: int) -> List[float]:
        user_row = self.get_user(uid)
        if not user_row:
            raise UnknownUserException
        return list(user_row[1:])

    def fill_places_table(self, n_places=N_SAMPLE_PLACES):
        for i in range(n_places):
            self.add_place(
                place_id=i,
                name=str(i),
                city='spb' if i % 2 else 'msk',
                indoor=bool(random.randint(0, 100) % 2),
                rating=random.uniform(1.0, 5.0),
                vec=list(np.random.rand(50))
            )

    def get_random_places(self, n_places: int, city: str, indoor_only=False, ):
        cursor = self.connection.cursor()
        if indoor_only:
            cursor.execute(GET_N_PLACES_BY_CITY_AND_TYPE_QUERY_TEMPLATE, (city, 1, n_places))
        else:
            cursor.execute(GET_N_PLACES_BY_CITY_QUERY_TEMPLATE, (city, n_places))
        rows = cursor.fetchall()
        cursor.close()
        return rows

