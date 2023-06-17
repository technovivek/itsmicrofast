from sqlalchemy.exc import SQLAlchemyError


class DatabaseError(Exception):

    def __init__(self, error):
        super().__init__(error)


class AlreayExistsInDBError(SQLAlchemyError):

    def __init__(self, error):
        super().__init__(error)

# The raise from statement in Python allows you to raise an exception
# while preserving the original exception's traceback. It is useful
# when you want to indicate that the current exception was caused
# by another exception.
