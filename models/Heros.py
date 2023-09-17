from sqlmodel import Field, String, Column, SQLModel
from typing import Optional


class Heros_(SQLModel, table=True):
    id: Optional[int] = Field(sa_column=Column(name="id", type_=int,
                                               primary_key=True, autoincrement=True,
                                               nullable=False))  # Field(primary_key= True, nullable= False)
    name: str = Field(sa_column=Column(name="name", type_=String(length=50)))
    secret_name: str = Field(sa_column=Column(name="secret_name", type_=String(length=50)))
    age: Optional[int] = Field(sa_column=Column(name="age", type_=int))
    team_id: Optional[int] = Field(sa_column=Column(name="team_id"), foreign_key="team.id")  # see here #some
    # heros that dont belong to a team
