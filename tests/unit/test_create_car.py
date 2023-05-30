import pytest

from operations.car import add_car_object, get_cars


from unittest.mock import Mock, patch

@patch('operations.car.uuid')
@patch('operations.car.select')
@patch('operations.car.sqlmodel_db_session')
def test_add_car_object(sql_session, select_mock,  uuid_mock):

    make = "test_make"
    model = "test_model"
    price = 900000.12

    select = Mock()
    select.return_value.where.return_value = None
    select_mock = select

    uuid_ = Mock()
    uuid_.uuid4 = Mock(return_value= "1234")
    uuid_mock.return_value = uuid_

    car = Mock()
    car.model = "Nano"

    with sql_session() as session:

        session.execute.return_value.fetchone = Mock(return_value=False)
        session.add.return_value = session
        # session.return_value.__enter__.return_value.execute.return_value.fetchone.return_value = "okay"
        # session.return_value.__enter__.return_value.add.return_value = None
        assert add_car_object(make = make, model = model, price = price) == {"id": str(uuid_mock.uuid4())}



@pytest.mark.parametrize('ret_val,expected',[([1,2],'Full')])
@patch('operations.create_car.db_session')
def test_get_car(session_mock, ret_val, expected):
    session = Mock()

    with session_mock() as session:
        # session.return_value.__enter
        session.query.return_value.all.return_value = ret_val
        session_mock.return_value = session

        assert expected in get_cars()




