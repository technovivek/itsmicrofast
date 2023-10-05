from sqlmodel import SQLModel
from fastapi import Body
import uuid
from datetime import datetime
from typing import Optional, List
from enum import Enum
from typing import Annotated


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHERS = "others"


class Base(SQLModel):
    pass


class PersonRequest(Base):
    first_name: Annotated[str, Body(max_length=50)]
    last_name: Annotated[str, Body(max_length=50)]
    gender: Annotated[Gender, Body()] = Gender.OTHERS.value
    email: Annotated[str, Body()]
    date_of_birth: Annotated[str, Body(regex= r"\d{4}-\d{2}-\d{2}", description="YYYY-MM-DD")]
    country_of_birth: Annotated[str, Body()]
    car_id: Annotated[Optional[uuid.UUID| str], Body()] = None
    # id: Annotated[uuid.UUID, Body()]


class CreatePersonResponse(Base):
    id: str


class Person(CreatePersonResponse):
    fname: str
    email: str


class ListPersons(List[Person]):
    pass
