from typing import Optional
from sqlmodel import SQLModel
from fastapi import Body


class Hero_(SQLModel):
    id: Optional[int] = Body(description= "ID of the hero")
    name: str = Body()
    secret_name: str
    age: int = Body()
    team_id: Optional[int] = Body(default= None, description= "ID of the team the hero belongs to")
