from models.team import Team_
from sqlalchemy.orm import Session


def add_team(db: Session, name: str, headquarters: str):
    team = Team_(name=name, headquarters=headquarters)
    db.add(team)
    db.commit()
    db.refresh(team)
    return team
