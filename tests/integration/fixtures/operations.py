from models.car import Car
import pytest


@pytest.fixture(scope="module")
def car_object():
    car = Car(make="make", model="model", price=32122.43)
    return car


@pytest.fixture(scope="module")
def person_attributes():
    person_attributes = {
        "first_name": "first_name",
        "last_name": "last_name",
        "gender": "gender",
        "email": "email",
        "date_of_birth": "date_of_birth",
        "country_of_birth": "country_of_birth",
        "car_id": "car_id",
    }
    return person_attributes
