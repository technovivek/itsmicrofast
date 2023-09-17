from typing import Optional
from sqlmodel import SQLModel
from fastapi import Body


class Team_(SQLModel):
    id: int = Body(description="Team ID")
    name: str
    headquarters: str | None = None
