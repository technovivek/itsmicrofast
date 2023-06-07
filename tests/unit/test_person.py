import pytest
from fastapi.exceptions import HTTPException
from models.person import Person
from unittest.mock import Mock, patch, call
from sqlalchemy.exc import DatabaseError
from operations.person import Person, sqlmodel_db_session, add_person, get_persons


@patch('operations.person.uuid')
@patch('operations.person.sqlmodel_db_session')
def test_add_person(session_mock, uuid_mock, person_attributes):
    uuid = Mock()
    uuid_mock.return_value = uuid

    with session_mock() as session:
        session.add.side_effect = [None, Exception("raised from here")]
        res = add_person(**person_attributes)
        assert isinstance(res, dict)
        assert "id" in res
        with pytest.raises(Exception):
            add_person(**person_attributes)
        session.add.assert_has_calls([call(Person(**person_attributes)),call(Person(**person_attributes))])
        uuid_mock.assert_has_calls([call.uuid4(), call.uuid4()])


#another way of patch
def test_add_person2(person_attributes):
    with patch('operations.person.sqlmodel_db_session') as session_mock:
        with patch('operations.person.uuid') as uuid_mock:
            uuid = Mock()
            uuid_mock.return_value = uuid
            with session_mock() as session:
                session.add.side_effect = [None, Exception("raised from here")]
                res = add_person(**person_attributes)
                assert isinstance(res, dict)
                assert "id" in res
                with pytest.raises(Exception):
                    add_person(**person_attributes)
                session.add.assert_has_calls([call(Person(**person_attributes)), call(Person(**person_attributes))])
                uuid_mock.assert_has_calls([call.uuid4(), call.uuid4()])


@patch('operations.person.select')
@patch('operations.person.sqlmodel_db_session')
def test_get_persons(session_mock, select_mock, person_attributes):

    person = Person(**person_attributes)

    with session_mock() as session:
        session.execute.return_value.fetchall.side_effect = [[[person]],[]]
        assert len(get_persons()) > 0
        assert [] == get_persons()
        session.execute.assert_has_calls([call(select_mock()), call().fetchall(), call(select_mock()), call().fetchall()])
        select_mock.assert_has_calls([call(Person), call(Person)])


