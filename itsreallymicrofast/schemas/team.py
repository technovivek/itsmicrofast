from sqlmodel import SQLModel, String, Field, Column, Integer, Relationship
from typing import List
from schemas.hero_team import Hero_Team_Link
from typing import TYPE_CHECKING
#https://sqlmodel.tiangolo.com/tutorial/code-structure/
if TYPE_CHECKING:
    from schemas.hero import Hero

# one to many
# class Team(SQLModel, table=True, ):
#     id: int = Field(sa_column=Column(name='id', type_=Integer, autoincrement=True, nullable=False, primary_key=True))
#     name: str = Field(sa_column=Column(nullable=False, type_=String, unique=True), max_length=100)
#     headquarters: str = Field(sa_column=Column(nullable=True, type_=String, unique=False), max_length=100)
#
#     # use of relationship
#     # relationship attributes gives you the entire object itself that is related.
#     # . they dont represent a column e.g hero.team
#     """Relationships are defined only on the SQLAlchemy side, not on the SQL side.
#     Simply create the tables or columns that you need, and the relationship will work correctly.
#     Therefore, it should not be in the migration."""
#     heros: List["Hero"] = Relationship(back_populates="team")


# the below class represents many to many relationship

class Team(SQLModel, table=True, ):
    id: int = Field(sa_column=Column(name='id', type_=Integer, autoincrement=True, default = None, primary_key=True))
    name: str = Field(sa_column=Column(nullable=False, type_=String, unique=True), max_length=100)
    headquarters: str = Field(sa_column=Column(nullable=True, type_=String, unique=False), max_length=100)
    heros: List["Hero"]|None = Relationship(back_populates="teams", link_model= Hero_Team_Link)
