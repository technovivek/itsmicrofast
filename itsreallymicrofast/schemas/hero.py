from sqlmodel import SQLModel, Field, Column, String, Integer, Relationship, ForeignKey
from typing import Optional, List
from schemas.team import Team
from schemas.hero_team import Hero_Team_Link


# the below class represents one to many relationship
# class Hero(SQLModel, table=True):
#     id: Optional[int] = Field(sa_column=Column(name="id", type_=Integer,
#                                                primary_key=True, autoincrement=True,
#                                                nullable=False))  # Field(primary_key= True, nullable= False)
#     name: str = Field(sa_column=Column(name="name", type_=String(length=50)))
#     secret_name: str = Field(sa_column=Column(name="secret_name", type_=String(length=50)))
#     age: Optional[int] = Field(sa_column=Column(name="age", type_=Integer))
#     team_id: Optional[int] = Field(
#         sa_column=Column(ForeignKey("team.id"), name="team_id", type_=Integer, nullable=True, default=None))
#
#     team: Optional[List["Team"]] = Relationship(back_populates="heros")
#     # see also  https://docs.sqlalchemy.org/en/20/orm/join_conditions.html
#     # team: "Team" = Relationship(back_populates="heros") this also os good

# the below class represents many to many relationship
class Hero(SQLModel, table=True):
    id: Optional[int] = Field(sa_column=Column(name="id", type_=Integer,
                                               primary_key=True, autoincrement=True,
                                               default = None))  # Field(primary_key= True, nullable= False)
    name: str = Field(sa_column=Column(name="name", type_=String(length=50)))
    secret_name: str = Field(sa_column=Column(name="secret_name", type_=String(length=50)))
    age: Optional[int] = Field(sa_column=Column(name="age", type_=Integer))

    teams: Optional[List["Team"]]| None = Relationship(back_populates="heros", link_model = Hero_Team_Link)

