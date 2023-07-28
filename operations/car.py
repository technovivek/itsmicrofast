import uuid
import random
from errors.database import AlreadyExistsInDBError
from db.database import sqlmodel_db_session

from sqlmodel import select, delete, Session, #or_, col

from models import Book
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
                   price: float, sunroof: bool) -> dict:
    try:
        # r = 1 / 0
        print("sunroof----->", sunroof)
        res = db.execute(select(Car).where(Car.model == model))
        print("Recess", [r for r in res])

        if [r for r in res]:
            raise AlreadyExistsInDBError(f"{model} already exists")
        id = uuid.uuid4()  # noqa A003
        car = Car(make=make, model=model, price=price, id=id, sunroof=sunroof)

        db.add(car)
        return {"id": str(id)}
    except AlreadyExistsInDBError as e:
        print("Operational error occurred", str(e))
        raise


def get_cars(session: Session) -> list[dict] | list:
    stmt = select(Car)
    res = session.exec(stmt)
    cars = res.all()
    if not res:
        return []
    else:

        return [
            {"id": f"{str(c.id)}", "make": c.make,
             "model": c.model}
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


def get_custom_values_from_car_reading_only():
    from db.database import sqlmodel_db_session

    with sqlmodel_db_session() as session:
        # stmt = select(Car).where(Car.price >=71000, Car.price < 30000000) #usage of and
        # stmt = select(Car).where(Car.model.in_(['Ignis','Harrier'])) #usage of in
        # stmt = select(Car).where(Car.model != "XYZ") #usage of != similarly >, >=, <, <=
        # stmt = select(Car).where(Car.price > 2000000, Car.price < 3500000) # and
        # stmt = select(Car).where(or_(col(Car.price) > 2000000, col(Car.price) < 3500000)) #or, Car.price can be treated as  None , it gives hint that it might be wrong. so we use col to tell editor that its a sqlmodel column
        # stmt =  select(Car).where(Car.sunroof == 't')
        stmt = select(Car).limit(2).offset(2)  # offset mtlb skip aur limit mtlb utna hi
        # stmt =  select(Car).where(Car.model=='Harrier') # use res.one() here.
        # There might be cases where we want to ensure that there's.
        # exactly one row matching the query. It returns an object too.
        # sqlalchemy.exc.MultipleResultsFound:
        # Multiple rows were found when exactly one was required when multiple rows are returned for one()
        # even when no rows are  found then it results in an error.

        # stmt = session.get(Car,"4748d37a-87cb-47d0-976a-9c41b214cc6d") # print(stmt) #shortcut to get via primary_key
        # print(stmt)
        res = session.exec(stmt)
        print(res.all())
        # res = session.exec(stmt).one()
        # print(res.first()) # to get the first. returns an object directly. None if not any result
        # print(res.one()) # to get all
        # print([r for r in res])


# get_custom_values_from_car_reading_only()

def get_custom_values_from_car_update_only():
    from db.database import sqlmodel_db_session

    with sqlmodel_db_session() as session:
        stmt = select(Car).where(Car.model == 'Harrier')
        car = session.exec(stmt).one()
        print("res", car)
        car.price = 2790900 #why the fuck it auto updates the values in the database
        car.sunroof = True
        session.add(car)
        session.commit()
        session.refresh(car)#explicit refresh. agar car.sunroon access karte to auto refresh ho jaata
        print(car)
        stmt2 = select(Car).where(Car.sunroof == True)
        #sessin.add_all([obj1, obj2, obj3])

get_custom_values_from_car_update_only()

def delete_values_from_book():


    with  sqlmodel_db_session() as session:
        stmt = select(Book).where(Book.title == 'sisi')
        book = session.exec(stmt).one()
        print("book-->", book)
        session.delete(book)
        session.commit()

        book = session.exec(select(Book).where(Book.title== 'sisi'))

        print("ghost  book", book.one())


delete_values_from_book()

#joining tables using sqlmodel


