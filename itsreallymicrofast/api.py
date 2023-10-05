from sqlmodel import select

from operations.team import Team
from operations.hero import Hero
from fastapi import FastAPI, Body, Depends
from models.team import Team, TeamResponse
from models.hero import Hero, HeroResponse
from http import HTTPStatus
from db.database import get_session, create_db_session
from sqlalchemy.orm import Session
from operations.team import add_team_to_db, get_team_from_db
from operations.hero import add_hero_to_db, get_hero_from_db, play_with_join

app = FastAPI(title="Hero and Team API")


@app.post("/team", response_model=TeamResponse, status_code=HTTPStatus.CREATED)
def add_team(team: Team, session: Session = Depends(get_session)):
    return add_team_to_db(db=session, **team.__dict__)


@app.post("/hero", response_model=HeroResponse, status_code=HTTPStatus.CREATED)
def add_hero(hero: Hero, session: Session = Depends(get_session)):
    return add_hero_to_db(db=session, **hero.__dict__)


@app.get("/teams/{team_id}", response_model=TeamResponse)
def fetch_team(team_id: int, session: Session = Depends(get_session)):
    return get_team_from_db(db=session, team_id=team_id)


@app.get("/heros/{hero_id}", )
def fetch_hero(hero_id: int, session: Session = Depends(get_session)):
    return get_hero_from_db(db=session, hero_id=hero_id)


@app.get("/play")
def just_play(db:Session = Depends(get_session)):
    return play_with_join(db= db)





