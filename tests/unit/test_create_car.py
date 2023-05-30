import pytest

from operations.car import create_car_object, get_car
# from models.car import Car
from unittest.mock import Mock, patch



@patch('operations.create_car.db_session')
def test_create_car_object(session_mock):
    session = Mock()
    with session_mock() as session:
        session.add.return_value = session
        session_mock.return_value = session
        assert create_car_object() == True

@pytest.mark.parametrize('ret_val,expected',[([1,2],'Full')])
@patch('operations.create_car.db_session')
def test_get_car(session_mock, ret_val, expected):
    session = Mock()

    with session_mock() as session:
        session.query.return_value.all.return_value = ret_val
        session_mock.return_value = session
        print("retttttt", ret_val)
        assert expected in get_car()




