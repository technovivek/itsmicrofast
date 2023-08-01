from sqlmodel import Field



class Team:
    id: int = Field(primary_key=True, nullable=False)
    name: str = Field(max_length=20, nullable=False, unique=True)
    headquarters: str = Field()
