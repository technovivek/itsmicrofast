from schemas.team import Team
from schemas.hero import Hero
from db.database import create_db_session
from sqlmodel import select


# def get_joined_data():
#     session = create_db_session()
#
#     stmt = select(Hero).join(Team).where(Team.id==Hero.team_id)
#     res = session.exec(stmt).all()
#     print("ress",res)
#     return res
#
#
# get_joined_data()
# populate the hero and the team tables with random data

def populate_hero_and_team():
    with create_db_session() as session:
        team1 = Team(id=1, name="Gatherer Team 1", headquarter="Gatherer Headquarter 1", )
        team2 = Team(id=2, name="Gatherer Team 2", headquarter="Gatherer Headquarter 2", )
        team3 = Team(id=3, name="Gatherer Team 3", headquarter="Gatherer Headquarter 3", )
        team4 = Team(id=4, name="Gatherer Team 4", headquarter="Gatherer Headquarter 4", )

        session.add(team1)
        session.add(team2)
        session.add(team3)
        session.add(team4)

        hero1 = Hero(id=1,name="Hero 1", secret_name="Secret Name 1", age=20, teams=[team1, team2, team4])
        hero2 = Hero(id=2,name="Hero 2", secret_name="Secret Name 2", age=20, teams=[team2, team4])
        hero3 = Hero(id = 3,name="Hero 3", secret_name="Secret Name 3", age=20, teams=[team1])
        hero4 = Hero(id=4,name="Hero 4", secret_name="Secret Name 4", age=20, teams=[])
        hero5 = Hero(id = 5,name="Hero 5", secret_name="Secret Name 5", age=20, teams=[team1, team3])
        hero6 = Hero(id = 6,name="Hero 6", secret_name="Secret Name 6", age=20, teams=[team2, team3])
        hero7 = Hero(id=7,name="Hero 7", secret_name="Secret Name 7", age=20, teams=[team1, team2])
        hero8 = Hero(id=8,name="Hero 8", secret_name="Secret Name 8", age=20, teams=[])
        hero9 = Hero(id=9,name="Hero 9", secret_name="Secret Name 9", age=20, teams=[team3])
        hero10 = Hero(id=10,name="Hero 10", secret_name="Secret Name 10", age=20, teams=[team4])
        hero11 = Hero(id=11,name="Hero 11", secret_name="Secret Name 11", age=20, teams=[team4])
        hero12 = Hero(id=12,name="Hero 12", secret_name="Secret Name 12", age=20, teams=[team4])

        session.add(hero1)
        session.add(hero2)
        session.add(hero3)
        session.add(hero4)
        session.add(hero5)
        session.add(hero6)
        session.add(hero7)
        session.add(hero8)
        session.add(hero9)
        session.add(hero10)
        session.add(hero11)
        session.add(hero12)



        session.commit()


# populate_hero_and_team()


def explore_back_populates():
    """
    say for example if we want to add hero12 to team 1, then it should also appear on the third table
    the new relationship

    :return:
    """
    with create_db_session() as session:
        hero = session.execute(select(Hero).where(Hero.id == 12)).one()[0]
        team = session.execute(select(Team).where(Team.id == 1)).one()[0]
        hero.teams.append(team)
        session.add(team)
        session.commit()
        for  t in hero.teams:
            print(t)
        #headquarters=None name='Gatherer Team 4' id=4
        #headquarters=None name='Gatherer Team 1' id=1


explore_back_populates()