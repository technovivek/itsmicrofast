from models.car import Car
from operations.car import add_car_object, delete_car_object, get_cars
# from models.car import Car
from unittest.mock import Mock, patch
from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy import select, delete


# def test_create_car_object():
#     assert create_car_object() == True

def test_add_car_object(session: Session, car_object):

    db = session
    id  = uuid4()
    db.add(car_object)
    db.commit()
    stmt  = select(Car).where(Car.model == car_object.model)
    res = db.execute(stmt)

    print("--->>",len([r for r in res]))

    db.execute(delete(Car).where(Car.id == id))
    assert  res is not None



