from db.database import Base
from sqlalchemy import  String,  Column, Integer, Numeric
from sqlmodel import Field, SQLModel
from pydantic import UUID4
from sqlalchemy.dialects.postgresql import UUID
import uuid

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
#           return f"Car {self.make}  model {self.model} id {self.id} price {self.price}"

class Car(SQLModel, table=True):


     #https://github.com/tiangolo/sqlmodel/issues/140

     id: uuid.UUID = Field(default_factory= uuid.uuid4, primary_key= True, nullable= False)
     make : str = Field(sa_column=Column(name = "make", type_ = String(length=50), nullable=False))
     model : str = Field(sa_column= Column(name = "model",type_=  String(length=50), nullable=False, unique= True))
     price : int = Field(sa_column=Column(name = "price", type_= Numeric))


     # def __repr__(self):
     #      return f"Car {Car.make}  model {Car.model} id {Car.id} price {Car.price}"
     #