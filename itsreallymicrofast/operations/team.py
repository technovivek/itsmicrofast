from schemas.team import Team
from sqlalchemy.orm import Session
from schemas.hero import Hero
from db.database import get_session


# v1
# def add_team_to_db(db: Session, id: int, name: str, headquarters: str):
#
#     """
#     see how we can utilze the relationships by adding team
#
#     hero_tarantula = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32, id = 111)
#     hero_dr_weird = Hero(name="Dr. Weird", secret_name="Steve Weird", age=36, id = 112)
#     hero_cap = Hero(
#         name="Captain North America", secret_name="Esteban Rogelios", age=93, id =113
#     )
#     team = Team(id= 18, name = "Heros Forever", headquarters = "Spain", heros = [hero_cap, hero_tarantula, hero_dr_weird])"""
#     team = Team(id=id, name= name, headquarters = headquarters)
#     db.add(team)
#     # db.add(hero)
#     db.commit()
#     db.refresh(team)
#     return {"name": team.name}


# v2
def add_team_to_db(db: Session, name: str, headquarters: str):
    """
    see how we can utilze the relationships by adding team

    hero_tarantula = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32, id = 111)
    hero_dr_weird = Hero(name="Dr. Weird", secret_name="Steve Weird", age=36, id = 112)
    hero_cap = Hero(
        name="Captain North America", secret_name="Esteban Rogelios", age=93, id =113
    )
    team = Team(id= 18, name = "Heros Forever", headquarters = "Spain", heros = [hero_cap, hero_tarantula, hero_dr_weird])"""

    team = Team(id=id, name=name, headquarters=headquarters)
    db.add(team)
    # db.add(hero)
    db.commit()
    db.refresh(team)
    return {"name": team.name}


def get_team_from_db(db: Session, team_id: int) -> Team:
    team = db.query(Team).where(Team.id == team_id).one_or_none()
    print("team@@@@@@@@@@@@@@@", [t.name for t in team.heros])
    return team

###################################################################################
def _get_team_from_db(team_id: int) -> Team:
    with get_session() as db:
        team = db.query(Team).where(Team.id == team_id).one_or_none()
        print("team@@@@@@@@@@@@@@@", [t.name for t in team.heros])
        return team


