import uuid

import pytest

from operations.car import add_car_object, get_cars, delete_car_object
from fastapi.exceptions import HTTPException
from models.car import Car

from unittest.mock import Mock, patch, call


@patch('operations.car.uuid')
@patch('operations.car.select')
@patch('operations.car.sqlmodel_db_session')
def test_add_car_object(sql_session, select_mock, uuid_mock):
    make = "test_make"
    model = "test_model"
    price = 900000.12

    # select = Mock()
    # select.return_value.where.return_value = None
    # select_mock = select

    uuid_ = Mock()
    uuid_.uuid4 = Mock(return_value="1234")
    uuid_mock.return_value = uuid_

    car = Mock()
    car.model = model
    car.make = make
    car.price = price

    select_ = Mock()
    select_.where.return_value = None
    select_mock.return_value = select_

    with sql_session() as session:
        session.execute.return_value.fetchone = Mock(side_effect=[False, True, True])
        # session.add.return_value = session
        session.add.side_effect = [session, Exception("raised from here"), HTTPException(status_code=500)]
        # session.return_value.__enter__.return_value.execute.return_value.fetchone.return_value = "okay"
        # session.return_value.__enter__.return_value.add.return_value = None
        assert add_car_object(make=make, model=model, price=price) == {"id": str(uuid_mock.uuid4())}
        uuid_mock.uuid4.assert_called()
        # sql_session.assert_called_once()
        session.execute.assert_called_once()
        with pytest.raises(Exception) as e:
            add_car_object(make=make, model=model, price=price)
        with pytest.raises(HTTPException):
            add_car_object(make=make, model=model, price=price)


# @pytest.mark.parametrize('ret_val,expected',[([1,2],'Full')])
@patch('operations.car.select')
@patch('operations.car.sqlmodel_db_session')
def test_get_car(session_mock, select_mock, car_object):
    with session_mock() as session:
        session.execute.return_value.all.side_effect = [[[car_object]], []]
        assert len(get_cars()) > 0
        assert [] == get_cars()
        session.execute.assert_called()
        select_mock.assert_called_with(Car)





def test_delete_car(car_object):
    id = uuid.uuid4()
    with patch('operations.car.sqlmodel_db_session') as session:
        with patch('operations.car.select') as select_mock:
            with patch('operations.car.delete') as delete_mock:
                select_mock.where.return_value = None
                delete_mock.where.return_value = None
                session.execute.side_effect = [True, False, True, Exception("raised from here")]
                assert isinstance(delete_car_object(id = id), HTTPException)
                with pytest.raises(Exception):
                    delete_car_object(id = id)
