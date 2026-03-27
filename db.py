from sqlmodel import Session,SQLModel,create_engine
from urllib.parse import quote_plus
from dotenv import load_dotenv
from fastapi import Depends
from typing import Annotated
import os
load_dotenv()

password = quote_plus(os.getenv("DB_PASSWORD"))


### SQLITE 3
# sqlitefilename = "mysqlitetest.db"
# sqliteurl = f"sqlite:///{sqlitefilename}"
# connect_args = {"check_same_thread": False}
# engine = create_engine(sqliteurl, connect_args=connect_args)

DATABASE_URL = f"mysql+pymysql://root:{password}@localhost:3306/fastapi"
engine = create_engine(DATABASE_URL)


def create_table_and_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
