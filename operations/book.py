from models.book import Book
from db.database import sqlmodel_db_session
from sqlmodel import select, Session


def add_book(session: Session):
    b = Book()
    print("before session", b, b.title)
    session.add(b)
    print("after session", b.id, b.title)
    session.commit()
    # https://sqlmodel.tiangolo.com/tutorial/automatic-id-none-refresh/
    # explicitly refreshing the data
    # In this case, after committing the object to the database with the session,
    # you could refresh it, and then return it to the client. This would ensure that the object has its fresh data.
    session.refresh(b)
    print("after committing the session", b.title, b.id)
    return "added"


def get_book(session: Session):

    stmt = select(Book)
    res = session.execute(stmt).first()
    print(res)
    return res
