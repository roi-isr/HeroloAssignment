from sqlalchemy.orm import declarative_base

Base = declarative_base()

from db import create_db_engine, create_db_session
from .__message import Message
from .__user import User

db_engine = create_db_engine()
DBSession = create_db_session(db_engine)

# create all table as described in the models package
Base.metadata.create_all(db_engine)
