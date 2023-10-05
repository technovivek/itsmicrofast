from sqlalchemy.orm import Session
from sqlmodel import SQLModel, create_engine
from sqlalchemy.exc import DatabaseError
import contextlib
from typing import Generator

db_settings = {
    "user": "postgres",
    "password": "admin",
    "host": "localhost",
    "port": "5432",
    "db": "dev03",
}


def _create_engine(database):
    database_url = (
        f"postgresql://{db_settings['user']}:{db_settings['password']}@{db_settings['host']}:"
        f"{db_settings['port']}/{database}"
    )

    return create_engine(database_url)


@contextlib.contextmanager
def create_db_session(db: str = db_settings['db']):
    session = None
    try:
        session = Session(bind=_create_engine(db))
        session.commit()
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        # SQLModel.metadata.create_all(bind=_create_engine())

        session.close()


def get_session() -> Generator[Session, None, None]:
    with create_db_session() as session:
        yield session
