
from sqlmodel import SQLModel

# class Team(SQLModel):
#     id: int
#     name: str
#     headquarters: str
#
# class TeamResponse(SQLModel):
#     name: str


#v2
class Team(SQLModel):

    name: str
    headquarters: str

class TeamResponse(SQLModel):
    name: str