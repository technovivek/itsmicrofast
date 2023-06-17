import contextlib

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import SQLModel

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


engine = create_test_db_conn()


@contextlib.contextmanager
def sqlmodel_db_session_for_test():
    session = None

    try:
        session = Session(bind=engine)
        yield session

    except Exception as e:
        session.rollback()
        SQLModel.metadata.drop_all(bind=engine)
        print("Exception occurred", str(e))
        raise e
    else:

        SQLModel.metadata.create_all(bind=engine)
        session.commit()
    # finally:
    #     session.close()


#
# @pytest.fixture(autouse= True)
# def db_session():
#     try:
#         with sqlmodel_db_session_for_test() as session:
#             yield session
#     finally:
#         SQLModel.metadata.drop_all(bind=engine)


class TestDatabase:
    def __init__(self):
        self.connection = sqlmodel_db_session_for_test

    def connect(self):
        return self.connection

    def add(self, entity):

        with self.connection() as session:
            session.add(entity)

    # def query(self, entity):
    #     with self.connection() as session:
    #         return session.query(entity)


@pytest.fixture
def test_database():
    # test_database = TestDatabase()
    # return test_database
    yield TestDatabase()
