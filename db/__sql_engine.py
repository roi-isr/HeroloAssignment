import os

from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


def create_db_engine():
    db_engine = create_engine(os.environ.get("DB_CONNECTION"))
    return db_engine


def create_db_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    return Session
