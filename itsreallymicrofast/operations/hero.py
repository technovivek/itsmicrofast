from sqlalchemy.orm import Session
from schemas.hero import Hero
from schemas.team import Team
from sqlmodel import select


# v1
# def add_hero_to_db(db: Session, id: int, name: str, secret_name: str, age: int, team_id: int):
#     hero = Hero(id=id, name=name, secret_name=secret_name, age=age, team_id=team_id)
#     db.add(hero)
#     db.commit()
#     db.refresh(hero)
#     return hero


# v2

def add_hero_to_db(db: Session, name: str, secret_name: str, age: int, team_id: int):
    hero = Hero(id=id, name=name, secret_name=secret_name, age=age, team_id=team_id)
    db.add(hero)
    db.commit()
    db.refresh(hero)
    return hero


def get_hero_from_db(db: Session, hero_id: int):
    res = db.query(Hero).where(Hero.id == hero_id).one_or_none()
    # get the team of the hero
    team = res.team
    print("team---->", team)

    return res

#extras
def play_with_join(db: Session):
    stmt = select(Hero, Team).join(Team, Hero.team_id == Team.id, isouter=True)
    # stmt = select(Hero, Team).join(Team, Hero.team_id == Team.id, isouter=True).where(Team.name == "Gatherer Team 5")
    """
    Notes:select ke andar jis table ka data chaaiye wo daalo.
    join me jisko join karna hai wo daalo and then the join condition
    we can use where with join to filter the data 
    if we want to break a connection simply assign the foregin key to None.
    
    """
    res = db.execute(stmt).all()
    for hero, team in res:
        print("Hero:", hero)
        print("Team:", team)
    return res
