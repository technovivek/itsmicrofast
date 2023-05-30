from datetime import datetime

from db.database import Base
# from sqlalchemy import Column, BigInteger, String, ForeignKey, Date
from sqlmodel import Column, String, Date, ForeignKey, Field, SQLModel
import uuid


class Person(SQLModel, table = True):



     # id = Column("id", BigInteger, primary_key= True)
     # first_name = Column("first_name",String(length=50), nullable=False)
     # last_name = Column("last_name",String(length=50), nullable=False)
     # gender = Column("gender",String(length=10), nullable=False)
     # email = Column("email", String(length=60))
     # date_of_birth = Column("dateofbirth", Date, nullable=False)
     # country_of_birth = Column("countryofbirth", String(length=50), nullable=False)
     # car_id = Column(BigInteger, ForeignKey("car.id"), unique=True)
     id: uuid.UUID = Field(primary_key= True, nullable= False, default_factory= uuid.uuid4)
     first_name: str = Field(sa_column=Column(type_ = String(length=50), nullable= False))
     last_name: str = Field(sa_column= Column(type_ = String(length=50), nullable=False))
     gender: str = Field(sa_column=Column(type_ = String(length=10), nullable=False))
     email: str = Field(sa_column=Column(type_ = String(length=60)))
     date_of_birth: datetime = Field(sa_column= Column(type_  = Date))
     country_of_birth: str = Field(sa_column= Column(nullable=False, type_ = String(50)))
     car_id: uuid.UUID = Field(sa_column=Column(ForeignKey("car.id"), unique=True))


     # def __repr__(self):
     #      return f"Person created with id : {Person.id}"
