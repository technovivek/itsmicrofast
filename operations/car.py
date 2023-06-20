import uuid
import random
from errors.database import AlreadyExistsInDBError

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
    try:
        # r = 1 / 0
        res = db.execute(select(Car).where(Car.model == model))
        print("Recess", [r for r in res])

        if res:
            raise AlreadyExistsInDBError(f"{model} already exists")
        id = uuid.uuid4()  # noqa A003
        car = Car(make=make, model=model, price=price, id=id)

        db.add(car)
        return {"id": str(id)}
    except AlreadyExistsInDBError as e:
        print("Operational error occurred", str(e))
        raise


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
                      id: uuid.UUID) -> None | list:  # noqa A003

    cars = [r for r in
            session.execute(select(Car).where(Car.id == id))]

    if len(cars) == 0:
        return []

    stmt = delete(Car).where(Car.id == id)
    session.execute(stmt)


def get_a_car(car_id: uuid.UUID, db: Session):
    car = db.query(Car).where(Car.id == car_id).one()
    print("----", car)
    return {"id": str(car_id), "make": "make", "model": "model"}

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
