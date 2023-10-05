from sqlmodel import SQLModel, Field, Integer, Column, ForeignKey
from typing import Optional


class Hero_Team_Link(SQLModel, table=True):
    hero_id: Optional[int] = Field(sa_column=Column(ForeignKey("hero.id"),primary_key=True, type_=Integer, default=None, ))
    team_id: Optional[int] = Field(sa_column=Column(ForeignKey("team.id"),primary_key=True, type_=Integer, default=None))



