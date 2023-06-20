# 1. async(will use Celery) 2. Annotated(done).  # Redis
# Flower #Docker # K8s #Pipelines #testing always
# JWT #poetry   #migration(alembic) #validator #Dependency management(done 1)
import uuid

from fastapi import FastAPI, status, Depends
from starlette.responses import JSONResponse
from operations.book import get_book, add_book

from operations.car import add_car_object, get_cars, \
    delete_car_object, get_a_car
from operations.person import add_person, get_persons
from schemas.car import SchemaCar, ListCars, CreateCarResponse, GetCar
from schemas.person import CreatePersonResponse, ListPersons, \
    PersonRequest
from db.database import get_session
# from models.car import Car
# from models.person import Person
from sqlalchemy.orm import Session
from enum import Enum

app = FastAPI(debug=True, title="Simple App")


class Tags(Enum):
    car = "Car"
    person = "Person"
    book = "Book"


@app.get("/")
def root():
    return "<h2>Hi There....</h2>"


@app.post(
    "/cars",
    tags=[Tags.car.value],
    status_code=status.HTTP_201_CREATED,
    response_model=CreateCarResponse,
)
def create_car(car: SchemaCar,
               session: Session = Depends(get_session)):
    print("-------", car.dict())

    res = add_car_object(session, make=car.make, model=car.model,
                         price=car.price)
    if not res:
        return JSONResponse(
            content="Failed!!",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return res


@app.get("/cars", tags=[Tags.car.value], response_model=ListCars)
def list_cars(session: Session = Depends(get_session)):
    res = get_cars(session)
    return res


@app.get("/cars/{car_id}", tags=[Tags.car.value], response_model=GetCar)
def get_single_car(car_id: uuid.UUID,
              session: Session = Depends(get_session)):
    res = get_a_car(car_id, session)
    return res


@app.post(
    "/person",
    tags=[Tags.person.value],
    status_code=status.HTTP_201_CREATED,
    response_model=CreatePersonResponse,
)
def add_person(input_: PersonRequest,
               session: Session = Depends(get_session)):
    res = add_person(session, **input_.__dict__)
    return res


@app.delete("/car/{id}", tags=[Tags.person.value],
            status_code=status.HTTP_204_NO_CONTENT)
def delete_car(id_: uuid.UUID,
               session: Session = Depends(get_session)):
    return delete_car_object(session, id_)


@app.get("/person", tags=[Tags.person.value], response_model=ListPersons)
def get_person(session: Session = Depends(get_session)):
    return get_persons(session)


@app.post("/books", tags=[Tags.book.value])
def create_book(session: Session = Depends(get_session)):
    return add_book(session)


@app.get("/books", tags=[Tags.book.value])
def get_books(session: Session = Depends(get_session)):
    return get_book(session)

#
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8002)
