from sqlmodel import Field
from typing import Optional
from sqlmodel import SQLModel
import uuid


class Book(SQLModel, table=True):

    # id : Optional[int] = Field(primary_key=True,default = None)
    id: Optional[uuid.UUID] = Field(primary_key=True, # noqa A003
                                    default_factory=uuid.uuid4)
    title: str = Field(max_length=20, default="Erried")
