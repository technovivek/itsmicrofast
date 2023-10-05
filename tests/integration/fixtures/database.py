import contextlib

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import SQLModel
from typing import Generator

# from models.car import Car
# from models.person import Person
Base = declarative_base()


def create_test_db_conn():
    db_settings = {
        "user": "postgres",
        "password": "admin",
        "host": "localhost",
        "port": "5432",
        "db": "test",
    }

    database_url = (
        f"postgresql://{db_settings['user']}:{db_settings['password']}@{db_settings['host']}:"
        f"{db_settings['port']}/{db_settings['db']}"
    )
    print("database url----->", database_url)

    engine = create_engine(database_url)
    return engine


@contextlib.contextmanager
def db_session_for_test() -> Generator:
    engine = None
    session = None
    try:
        engine = create_test_db_conn()
        session = Session(bind=engine)
        yield session
    finally:
        SQLModel.metadata.create_all(bind=engine)
        session.commit()
        # session.rollback()
        # SQLModel.metadata.drop_all(bind=engine)



@pytest.fixture(scope="module")
def get_test_session() -> Generator[Session, None, None]:
    with db_session_for_test() as session:
        yield session
