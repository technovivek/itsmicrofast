import uuid
from time import sleep

from fastapi.exceptions import HTTPException
from fastapi import status
from typing import List, Dict, Any

from schemas.car import CreateCarResponse, CarResponseBase, ListCars

from sqlmodel import select

from models.car import Car
# from db.database import db_session
from db.database import sqlmodel_db_session
from uuid import uuid4

car_models = [
    "Camry",
    "Civic",
    "Mustang",
    "Corvette",
    "Series",
    "C-Class",
    "A4",
    "Golf",
    "Outback",
    "Wrangler",
    "LeRX",
    "Sonata",
    "Mazda3",
    "Altima",
    "VXC90",
    "Model S",
    "Sportage",
    "Sierra",
    "Escalade",
    "Chrysler 300"
]

car_makes = [
    "Toyota",
    "Honda",
    "Ford",
    "Chevrolet",
    "Nissan",
    "BMW",
    "Mercedes-Benz",
    "Audi",
    "Volkswagen",
    "Hyundai",
    "Kia",
    "Mazda",
    "Subaru",
    "Volvo",
    "Lexus",
    "Jeep",
    "Chrysler",
    "Tesla",
    "Land Rover",
    "Jaguar"
]
import random
price_list = [random.choice([r for r in range(1000000, 9999999)]) for r in range(20)]
print("price_list", price_list)


#for one time. for filling up db auto
# def create_car_object():
#
#     with sqlmodel_db_session() as session:
#         for i in range(20):
#             car = Car(make = car_makes[i], model = car_models[i], price = price_list[i], id = uuid4())
#             session.add(car)
#         # print(f"{car1.make} added")
#         return True

def add_car_object(make, model, price) -> dict:





    id = uuid.uuid4()
    car = Car(make=make, model=model, price=price, id=id)

    try:

        with sqlmodel_db_session() as session:
            #perform a check
            stmt = select(Car).where(Car.model == model)
            res =  session.execute(stmt).fetchone()
            if res:
                raise HTTPException(detail = "Model already present!" , status_code= status.HTTP_409_CONFLICT)
            else:
                session.add(car)
                return {"id": str(id)}
    except Exception as e:

        print("Failed to add to DB", str(e))
        raise  e



def get_cars() -> list[dict] | list:
    with sqlmodel_db_session()  as session:
        stmt = select(Car)
        res = session.execute(stmt)
        cars = res.all()
        if not res:
            return []
        else:

            return [{"id": f'{str(c[0].id)}', "make":c[0].make, "model": c[0].model } for c in cars]

#when using sqlalchemy
# def get_car():
#
#     with sqlmodel_db_session() as session:
#         stmt = select(Car).where(Car.id == 3)
#         res = session.exec(stmt)
#         if res:
#             # for r in res:
#             #     print(r)
#             return [r for r in res]
#         else:
#             []

# create_car_object()
# print(get_car())