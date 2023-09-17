from models.Heros import Heros_
from db.database import get_session
from sqlalchemy.orm import Session
from typing import Optional


def add_heros_to_db(session: Session, id: Optional[int], name: str, secret_name: str, age: Optional[int],
                    team_id: Optional[int]):
    hero = Heros_(name=name, secret_name=secret_name, age=age, team_id=team_id, id=id)
    session.add(hero)
    session.commit()
