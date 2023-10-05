from fastapi import Body
from sqlmodel import SQLModel
from typing import Optional

#v1
# class Hero(SQLModel):
#     id: int
#     name: str
#     secret_name: str
#     age: int = Body(gt=15, lt=100)
#     team_id: Optional[int] = Body(default=None, description="ID of the team the hero belongs to")
#
#
# class HeroResponse(Hero):
#     pass


#v2
class Hero(SQLModel):

    name: str
    secret_name: str
    age: int = Body(gt=15, lt=100)
    team_id: Optional[int] = Body(default=None, description="ID of the team the hero belongs to")


class HeroResponse(Hero):
    pass

