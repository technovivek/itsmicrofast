from sqlmodel import SQLModel
from fastapi import Body
from typing import List
from typing import Annotated, Optional


class Base(SQLModel):
    pass


class CarResponseBase(SQLModel):
    id: str  # noqa A003


class SchemaCar(Base):
    # make: str = Body(min_length= 3, max_length= 50)
    # just to show the usage of Annotated. Annotated is
    # just a newer expression of hinting in pydantic
    make: Annotated[
        str, Body(min_length=3, max_length=50)
    ] = ...  # just to keep in mind that this is how Annotation works
    model: Annotated[str, Body(min_length=3, max_length=50)] = ...
    price: Annotated[float, Body(example=8989889)]
    sunroof: Optional[Annotated[bool, Body(example=False)]] = False

    # id: uuid.UUID| None = Body(default=uuid.uuid4())
    class Config:
        schema_extra = {
            "example": {
                "make": "Foo",
                "model": "Baar",
                "price": 6585785,
                "sunroof": False,
            }
        }


class CreateCarResponse(CarResponseBase):
    pass


class GetCar(CarResponseBase):
    make: str
    model: str


class ListCars(List[GetCar]):
    pass
