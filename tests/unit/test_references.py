from dataclasses import dataclass
from unittest.mock import Mock, patch

#place where we need to patch a dictionary
mydict = {'a':1}
@patch.dict(mydict, {'b':2}, clear=True)
def test_dict():
    print("f--->", mydict)
    assert 'b' in mydict.keys()
    assert 'a' in mydict.keys()

@dataclass
class DatabaseSettings:
    user: str
    password: str
    host: str
    port: int
    db: str

settings = DatabaseSettings(user='', password='',host='',port=5432,db='')

def test_db_settings():
    with patch.multiple(settings, host='198.23.43.444'):
        print(settings)

def test_db_set_with_obj():
    with patch.object(settings, "user",'ram'):
        print(settings.user)

