from sqlmodel import Field, Column, SQLModel



class Team(SQLModel, table=True):
    id: int = Field(sa_column=Column(primary_key= True,type_ = int ,nullable= False, autoincrement= True))#Field(primary_key=True, nullable=False)
    name: str = Field(sa_column=Column(nullable= False, type_=str, unique= True), max_length= 50)
    headquarters: str = Field(sa_column=Column(nullable= True, type_=str, unique= False), max_length= 50)
