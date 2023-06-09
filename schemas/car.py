from sqlmodel import SQLModel
from fastapi import Body
import uuid
from typing import List
from pydantic.generics import GenericModel
from typing import Annotated


class Base(SQLModel):
    pass


class CarResponseBase(SQLModel):
    id: str


class SchemaCar(Base):
    # make: str = Body(min_length= 3, max_length= 50)
    # just to show the usage of Annotated. Annotated is just a newer expression of hinting in pydantic
    make: Annotated[
        str, Body(min_length=3, max_length=50)] = ...  # just to keep in mind that this is how Annotation works
    model: Annotated[str, Body(min_length=3, max_length=50)] = ...
    price: Annotated[float, Body(example=8989889)]

    # id: uuid.UUID| None = Body(default=uuid.uuid4())
    class Config:
        schema_extra = {
            "example": {
                "make": "Foo",
                "model": "Baar",
                "price": 6585785,

            }
        }


class CreateCarResponse(CarResponseBase):
    pass


class ListCars(List[CarResponseBase]):
    make: str
    model: str
