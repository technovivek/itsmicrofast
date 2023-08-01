from typing import Optional
from sqlmodel import SQLModel
from fastapi import Body


class Team(SQLModel):
    id: int = Body(description="Team ID")
    name: str = Body()
    headquarters: Optional[str] = Body()
