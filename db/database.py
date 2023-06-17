import contextlib
from dataclasses import dataclass

from typing import Generator

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import create_engine, Session, SQLModel


# This wouldn't work! 🚨
# from sqlmodel import SQLModel
#
# from .db import engine
#
# SQLModel.metadata.create_all(engine)
# It wouldn't work because when you import SQLModel alone,
# Python doesn't execute all the code creating the classes inheriting.
# from it (in our example, the class Hero),
# so SQLModel.metadata is still empty.


@dataclass
class DatabaseSettings:
    user: str
    password: str
    host: str
    port: int
    db: str


def create_db_engine():
    db_settings = {
        "user": "postgres",
        "password": "admin",
        "host": "localhost",
        "port": "5432",
        "db": "dev02",
    }

    database_url = (
        f"postgresql://{db_settings['user']}:{db_settings['password']}@{db_settings['host']}:"
        f"{db_settings['port']}/{db_settings['db']}"
    )
    # print("database url----->", database_url)

    engine = create_engine(database_url)
    return engine


@contextlib.contextmanager
def sqlmodel_db_session():
    session = None
    engine = create_db_engine()
    try:
        session = Session(bind=engine, expire_on_commit=False)
        yield session

    finally:
        SQLModel.metadata.create_all(bind=engine)
        session.commit()
        session.close()


# Generator[YieldType, SendType, ReturnType]
def get_session() -> Generator[Session, None, None]:
    try:
        with sqlmodel_db_session() as session:
            yield session

    except SQLAlchemyError as e:
        raise e
