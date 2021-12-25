from main.dbservice import DatabaseService, VEC_SIZE


def test_places_add():
    service = DatabaseService()
    service.init_places_table()
    place_id = 111
    place_name = '111'
    city = 'spb'
    indoor = True
    rating = 3.0
    vec = [0.0 for _ in range(50)]
    service.add_place(place_id=place_id,
                name=place_name,
                city=city,
                indoor=indoor,
                rating=rating,
                vec=vec
    )
    place = service.get_place(111)
    assert place[0] == place_id
    assert place[1] == place_name
    assert place[2] == city
    assert place[3] == indoor
    assert place[4] == rating
    vec_real = list(place[-50:])
    assert len(vec_real) == len(vec)
    for i in range(len(vec)):
        assert vec_real[i] == vec[i]
    service.close_connection()


def test_get_places_by_city():
    service = DatabaseService()
    service.init_places_table()
    service.fill_places_table()
    city = 'msk'
    random_places = service.get_random_places(10, city)
    for place in random_places:
        assert place[2] == city
    service.close_connection()


def test_get_places_by_city_only_indoor():
    service = DatabaseService()
    service.init_places_table()
    service.fill_places_table()
    city = 'spb'
    random_places = service.get_random_places(10, city, indoor_only=True)
    for place in random_places:
        assert place[2] == city
        assert place[3] == True
    service.close_connection()


def test_users():
    service = DatabaseService()
    service.init_users_table()
    uid = 111
    vec = [1.0 for _ in range(VEC_SIZE)]
    service.add_user(uid, vec)
    user = service.get_user(uid)
    assert user[0] == uid
    vec_real = list(user[-50:])
    assert len(vec_real) == len(vec)
    for i in range(len(vec)):
        assert vec_real[i] == vec[i]
    service.close_connection()
