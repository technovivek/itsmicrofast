from operations.car import create_car_object
# from models.car import Car
from unittest.mock import Mock, patch


# def test_create_car_object():
#     assert create_car_object() == True

def test_create_car_object(session):

    # car = Car(id=11, make="Hondaa", model="Amazee", price="900040.6")
    with patch('operations.create_car.db_session',session):
        assert create_car_object() == True



