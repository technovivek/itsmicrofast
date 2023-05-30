import contextlib

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base


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
def session_for_test():
    session = None
    engine = create_test_db_conn()
    try:
        session = Session(bind=engine)
        yield session


    except Exception as e:
        session.rollback()
        print("Exception occured", str(e))
    finally:
        Base = declarative_base()
        Base.metadata.create_all(bind=engine)
        print("session rolled backed!!!")
        session.close()

@pytest.fixture
def session():
    yield session_for_test
