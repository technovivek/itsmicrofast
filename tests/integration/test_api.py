import uuid

import pytest
from starlette import status


def test_root(test_app_client):
    response =  test_app_client.get("/")
    assert response.json() == "<h2>Hi There....</h2>"
    assert response.status_code == 200


def test_create_car(get_test_session, test_app_client):

    car_id = uuid.uuid4()

    json_data = {

                "make": "Foo",
                "model": "Baar",
                "price": 6585785,
                "is_sunroof": "False",
                "id": car_id
                }
    response = test_app_client.post("/cars", json = json_data)
    assert response.status_code == status.HTTP_201_CREATED





