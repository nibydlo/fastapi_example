import sqlite3
from typing import Optional, Tuple

import service

INIT_SCRIPT = """
DROP TABLE IF EXISTS places;

CREATE TABLE places (
    place_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    region_id INTEGER NOT NULL,
    type INTEGER NOT NULL,
    is_test BOOL NOT NULL);
"""

ADD_PLACE_QUERY_TEMPLATE = """INSERT INTO places (place_id, name, region_id, type, is_test) VALUES (?, ?, ?, ?, ?)"""
GET_ALL_PLACES_QUERY = """SELECT * FROM places"""
GET_PLACE_QUERY_TEMPLATE = """SELECT * FROM places WHERE place_id = ?"""
GET_PLACES_BY_REGION_QUERY_TEMPLATE = """SELECT * FROM places WHERE region_id = ?"""
DELETE_PLACE_QUERY_TEMPLATE = """DELETE FROM places WHERE place_id = ?"""
DELETE_TEST_QUERY_TEMPLATE = """DELETE FROM places WHERE is_test = TRUE"""
DEFAULT_PATH = '.\\db.sqlite'


class DatabaseService():
    def __init__(self, path: str = DEFAULT_PATH):
        self.path = path
        self.connection = self.create_connection()

    def create_connection(self) -> Optional[sqlite3.Connection]:
        try:
            connection = sqlite3.connect(self.path)
            return connection
        except sqlite3.Error as e:
            print(f'Error while creating db connection: {e}')

    def close_connection(self):
        self.connection.close()

    def init_events_table(self):
        cursor = self.connection.cursor()
        cursor.executescript(INIT_SCRIPT)
        self.connection.commit()
        cursor.close()

    def __run_query_void(self, query_template: str, args: Tuple):
        cursor = self.connection.cursor()
        cursor.execute(query_template, args)
        self.connection.commit()
        cursor.close()

    def add_place(self, place_id: int, name: str, region_id: int, type: service.PlaceType, is_test: bool = False):
        self.__run_query_void(ADD_PLACE_QUERY_TEMPLATE, (place_id, name, region_id, type.value, is_test))

    def delete_place(self, place_id: int):
        self.__run_query_void(DELETE_PLACE_QUERY_TEMPLATE, (place_id,))

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
        cursor.execute(GET_PLACE_QUERY_TEMPLATE, (place_id, ))
        row = cursor.fetchone()
        cursor.close()
        return row

    def get_places_by_region(self, region_id: int) -> list:
        cursor = self.connection.cursor()
        cursor.execute(GET_PLACES_BY_REGION_QUERY_TEMPLATE, (region_id, ))
        rows = cursor.fetchall()
        cursor.close()
        return rows
