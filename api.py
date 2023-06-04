# 1. async(will use Celery) 2. Annotated(done).  # Redis
# Flower #Docker # K8s #Pipelines #testing always
# JWT #poetry   #migration(alembic) #validator #Dependency management
import uuid

from fastapi import FastAPI, status
from starlette.responses import JSONResponse
from operations.book import get_book, add_book

from operations.car import add_car_object, get_cars, delete_car_object
from operations.person import add_person, get_persons
from schemas.car import SchemaCar, ListCars, CreateCarResponse
from schemas.person import CreatePersonResponse, ListPersons, PersonRequest

app = FastAPI(debug=True, title="Simple App")


@app.get("/")
def root():
    return "<h2>Hi There....</h2>"


@app.post("/cars", tags=["Cars", "Person"], status_code=status.HTTP_201_CREATED, response_model=CreateCarResponse)
def create_car(request: SchemaCar):
    print("-------", request.dict())

    res = add_car_object(make=request.make, model=request.model, price=request.price)
    if not res:
        return JSONResponse(content="Failed!!", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return res


@app.get("/cars", tags=["Cars"], response_model=ListCars)
def list_cars():
    res = get_cars()
    return res


@app.post("/person", tags=["Person"], status_code=status.HTTP_201_CREATED, response_model=CreatePersonResponse)
def add_person(input: PersonRequest):
    res = add_person(**input.__dict__)
    return res

@app.delete("/car/{id}", tags=["Person"], status_code= status.HTTP_204_NO_CONTENT)
def delete_car(id: uuid.UUID):
    return delete_car_object(id)


@app.get("/person", tags=["Person"], response_model=ListPersons)
def get_person():
    return get_persons()


@app.post("/books", tags=["Book"])
def create_book():
    return add_book()


@app.get("/books", tags=["Book"])
def get_books():
    return get_book()

#
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8002)
