from models.car import Car
from operations.car import add_car_object, delete_car_object, get_cars, sqlmodel_db_session
# from models.car import Car
from unittest.mock import Mock, patch
from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy import select, delete


# def test_create_car_object():
#     assert create_car_object() == True

@patch('operations.car.sqlmodel_db_session')
def test_add_car_object(sql_mock,test_database,car_object):

    sql = Mock(return_value= test_database.connect())
    sql_mock.__enter__.return_value = sql


    # test_database.add(car_object)

    assert "id" in add_car_object(make= car_object.make, model = car_object.model, price=car_object.price)



def test_added_car(test_database, car_object):

    sess= test_database.connect()
    with sess() as session:
        stmt = select(Car).where(Car.model == car_object.model)
        res = session.execute(stmt).all()
        assert len(res) > 0





    # test_database.add(car_object)
    # print("res---->", [r for r in test_database.query(car_object) if r.model == car_object.model])
    # with db_session() as session:
    # stmt = select(Car).where(Car.model == car_object.model)
    # res = db_session.execute(stmt)
    # print("re-----", res)



    # with test_database.connection() as session:
    #     stmt = select(Car).where(Car.model == car_object.model)
    #     res = session.execute(stmt)
    #     print("re-----", res)




