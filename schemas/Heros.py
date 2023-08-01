from typing import Optional
from sqlmodel import SQLModel
from fastapi import Body


class Hero(SQLModel):
    id: Optional[int] = Body(description= "ID of the hero")
    name: str = Body()
    secret_name: str = Body()
    age: int = Body()
    team_id: Optional[int] = Body()
