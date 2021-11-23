import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()


def create_db_engine():
    db_engine = create_engine(os.environ.get("DATABASE_URL_1"))
    return db_engine


def create_db_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    return Session


def open_db_session(DBSession):
    db_session = DBSession()
    db_session.autoflush = True
    return db_session


def write(db_session, model_instance):
    db_session.add(model_instance)
    db_session.commit()
