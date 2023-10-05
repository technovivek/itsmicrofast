from sqlalchemy import String, Column, Numeric, Boolean
from sqlmodel import Field, SQLModel
import uuid
from typing import Optional


# class Car(Base):
#
#      __tablename__ = 'car'
#
#      id = Column("id",BigInteger , primary_key=True)
#      make = Column("make", String(length=50), nullable=False)
#      model = Column("model", String(length=50), nullable=False)
#      price = Column("price", Numeric(20,2))
#
#      def __init__(self, id, make, model, price) -> None:
#           self.id = id
#           self.make = make
#           self.model = model
#           self.price = price
#
#      def __repr__(self):
#           return f"Car {self.make}  model {self.model}
#           id {self.id} price {self.price}"


class Car(SQLModel, table=True):
    # https://github.com/tiangolo/sqlmodel/issues/140

    id: uuid.UUID = Field(default_factory=uuid.uuid4, # noqa A003
                          primary_key=True, nullable=False)
    make: str = Field(
        sa_column=Column(name="make", type_=String(length=50),
                         nullable=False)
    )
    model: str = Field(
        sa_column=Column(
            name="model", type_=String(length=50), nullable=False, unique=True
        ),
        index=True,
    )
    price: int = Field(sa_column=Column(name="price", type_=Numeric))
    sunroof: Optional[bool] = Field(sa_column=Column(name="is_sunroof", type_=Boolean, default= False))

    # def __repr__(self):
    #      return f"Car {Car.make}  model {Car.model} id {Car.id} price {Car.price}"
    #
