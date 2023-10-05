from sqlmodel import SQLModel, Field, Column, Integer, String, Relationship, ForeignKey
from typing import List, Optional


class Users(SQLModel, table=True):
    id: int = Field(sa_column=Column('id', autoincrement=True, primary_key=True, nullable=False, type_=Integer))
    name: str = Field(sa_column=Column('user_name', type_=String(length=50)))
    roles: Optional[List["roles"]] = Relationship(back_populates="users")


class Roles(SQLModel, table=True):
    id: int = Field(sa_column=Column('id', type_=Integer, primary_key=True, nullable=False, autoincrement=True))
    name: str = Field(sa_column=Column('role_name', type_=String()))
    users: str = Relationship(back_populates="roles")


class UserRoles(SQLModel, table=True):
    user_id: int = ForeignKey("user.id")
    role_id: int = ForeignKey("role.id")
    roles: Roles = Relationship(back_populates="roles")
    heros: Users = Relationship(back_populates="users")
