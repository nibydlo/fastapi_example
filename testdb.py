import pytest
from service import PlaceType
from dbservice import DatabaseService


def test_add_get_all():
    service = DatabaseService()
    service.init_events_table()
    service.add_place(111, 'place_1', 1, PlaceType.INDOOR, True)
    service.add_place(122, 'place_2', 2, PlaceType.OUTDOOR, True)
    places = service.get_all_places()
    assert len(places) == 2
    place_1 = places[0]
    assert place_1[0] == 111
    assert place_1[1] == 'place_1'
    assert place_1[2] == 1
    assert place_1[3] == PlaceType.INDOOR.value
    place_2 = places[1]
    assert place_2[0] == 122
    assert place_2[1] == 'place_2'
    assert place_2[2] == 2
    assert place_2[3] == PlaceType.OUTDOOR.value
    service.delete_test()
    service.close_connection()


def test_add_get():
    service = DatabaseService()
    service.init_events_table()
    service.add_place(111, 'place_1', 1, PlaceType.INDOOR, True)
    place_1 = service.get_place(111)
    assert place_1[0] == 111
    assert place_1[1] == 'place_1'
    assert place_1[2] == 1
    assert place_1[3] == PlaceType.INDOOR.value
    service.delete_test()
    service.close_connection()


def test_add_get_by_region():
    service = DatabaseService()
    service.init_events_table()
    service.add_place(111, 'place_1', 1, PlaceType.INDOOR, True)
    service.add_place(211, 'place_2', 1, PlaceType.INDOOR, True)
    service.add_place(122, 'place_3', 2, PlaceType.OUTDOOR, True)
    places = service.get_places_by_region(1)
    assert len(places) == 2
    place_1 = places[0]
    assert place_1[0] == 111
    assert place_1[1] == 'place_1'
    assert place_1[2] == 1
    assert place_1[3] == PlaceType.INDOOR.value
    place_2 = places[1]
    assert place_2[0] == 211
    assert place_2[1] == 'place_2'
    assert place_2[2] == 1
    assert place_2[3] == PlaceType.INDOOR.value
    service.delete_test()
    service.close_connection()


def test_add_delete():
    service = DatabaseService()
    service.init_events_table()
    service.add_place(111, 'place_1', 1, PlaceType.INDOOR, True)
    service.add_place(122, 'place_2', 2, PlaceType.OUTDOOR, True)
    service.delete_place(122)
    places = service.get_all_places()
    assert len(places) == 1
    place_1 = places[0]
    assert place_1[0] == 111
    assert place_1[1] == 'place_1'
    assert place_1[2] == 1
    assert place_1[3] == PlaceType.INDOOR.value
    service.delete_test()
    service.close_connection()
