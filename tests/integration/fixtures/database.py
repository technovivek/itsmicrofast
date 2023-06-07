import contextlib

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import SQLModel


def create_test_db_conn():
    db_settings = {"user": "postgres",
                   "password": "admin",
                   "host": "localhost",
                   "port": "5432",
                   "db": "test"}

    database_url = f"postgresql://{db_settings['user']}:{db_settings['password']}@{db_settings['host']}:" \
                   f"{db_settings['port']}/{db_settings['db']}"
    print("database url----->", database_url)

    engine = create_engine(database_url)
    return engine

@contextlib.contextmanager
def sqlmodel_db_session_for_test():
    session = None
    engine = create_test_db_conn()
    try:
        session = Session(bind=engine)
        yield session


    except Exception as e:
        session.rollback()
        print("Exception occured", str(e))
        raise e
    finally:
        SQLModel.metadata.create_all(bind= engine)
        session.commit()
        session.close()

@pytest.fixture
def session():
    with sqlmodel_db_session_for_test() as session:
        yield session
