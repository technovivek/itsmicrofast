import uuid
import random
from fastapi.exceptions import HTTPException
from fastapi import status
from errors.database import AlreayExistsInDBError

from sqlmodel import select, delete, Session

from models.car import Car

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
    "Chrysler 300",
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
    "Jaguar",
]


price_list = [random.choice([r for r in range(1000000, 9999999)]) for
              r in range(20)]


# print("price_list", price_list)


# for one time. for filling up db auto
# def create_car_object():
#
#     with sqlmodel_db_session() as session:
#         for i in range(20):
#             car = Car(make = car_makes[i], model = car_models[i],
#             price = price_list[i], id = uuid4())
#             session.add(car)
#         # print(f"{car1.make} added")
#         return True

# V1
# def add_car_object(make: str, model: str, price: float) -> dict:
#     id = uuid.uuid4()
#     car = Car(make=make, model=model, price=price, id=id)
#
#     try:
#
#         with sqlmodel_db_session() as session:
#             session.add(car)
#         return {"id": str(id)}
#     except Exception as i:
#
#         print("Failed to add to DB", str(i))
#         raise
# v2


def add_car_object(db: Session, make: str, model: str,
                   price: float) -> dict:

    if db.query(Car).where(Car.model == model):
        raise AlreayExistsInDBError(f"{model} already exists")
    id = uuid.uuid4()  # noqa A003
    car = Car(make=make, model=model, price=price, id=id)
    # car = Car.from_orm()

    db.add(car)
    return {"id": str(id)}


def get_cars(session: Session) -> list[dict] | list:
    stmt = select(Car)
    res = session.execute(stmt)
    cars = res.all()
    if not res:
        return []
    else:

        return [
            {"id": f"{str(c[0].id)}", "make": c[0].make,
             "model": c[0].model}
            for c in cars
        ]


def delete_car_object(session: Session,
                      id: uuid.UUID) -> HTTPException | None: # noqa A003
    try:

        if not session.execute(select(Car).where(Car.id == id)):
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found"
            )
        stmt = delete(Car).where(Car.id == id)
        session.execute(stmt)

    except Exception as d:
        print("deletion not performed", str(d))
        raise

# when using sqlalchemy
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
