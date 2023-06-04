from models.car import Car
from models.person import Person
from unittest.mock import Mock
import pytest

@pytest.fixture(scope='module')
def car_object():
    car = Car(make="make",model = "model", price = 32122.43)
    return car

@pytest.fixture(scope='module')
def person_attributes():
    # person = Person(first_name = "first_name",
    #                         last_name = "last_name",
    #                         gender = "gender",
    #                         email = "email",
    #                         date_of_birth = "date_of_birth",
    #                         country_of_birth = "country_of_birth", car_id = "car_id",id = 1234
    person_attributes = {"first_name" : "first_name",
                                      "last_name" : "last_name",
                                                  "gender" : "gender",
                                                           "email" : "email",
                                                                   "date_of_birth" : "date_of_birth",
                                                                                   "country_of_birth" : "country_of_birth",
                         "car_id" : "car_id"}
    return person_attributes