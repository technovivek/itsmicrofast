from sqlmodel import Field
from typing import Optional

class Heros:
    id: Optional[int] = Field(primary_key= True, nullable= False)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default= None, index=True)
    team_id: Optional[int] = Field(default = None, foreign_key= "team.id") #see here #some
    #heros that dont belong to a team