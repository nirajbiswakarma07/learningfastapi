from fastapi import FastAPI,HTTPException,Depends,Query,status
from contextlib import asynccontextmanager
from sqlmodel import Session,select
from typing import Annotated
from sqlmodel import Session


from models import Hero,HeroCreate,HeroRead,HeroUpdate
from db import create_table_and_db,get_session


SessionDep = Annotated[Session,Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):    
    create_table_and_db()
    print("App started")
    yield
    print("App stopped")


app = FastAPI(lifespan=lifespan)


@app.post("/heroes",tags=["Heroes"],status_code=status.HTTP_201_CREATED,response_model=HeroRead)
async def create_hero(hero: HeroCreate, session: SessionDep):
    db_hero = Hero.model_validate(hero) 
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

@app.get("/heroes",tags=["Heroes"],status_code=status.HTTP_200_OK)
async def create_hero(session:SessionDep):
    statement = select(Hero)
    heroes = session.exec(statement).all()
    return heroes


@app.patch("/heroes/{hero_id}", tags=["Heroes"],status_code=status.HTTP_200_OK,response_model=HeroRead)
async def patch_hero(hero_id: int, hero: HeroUpdate, session: SessionDep):
    db_hero = session.get(Hero, hero_id)
    
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    hero_data = hero.model_dump(exclude_unset=True)

    for key, value in hero_data.items():
        setattr(db_hero, key, value)

    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)

    return db_hero


@app.delete("/heroes/{hero_id}", tags=["Heroes"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_hero(hero_id: int, session: SessionDep):
    db_hero = session.get(Hero, hero_id)
    
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    session.delete(db_hero)
    session.commit()
    
    return