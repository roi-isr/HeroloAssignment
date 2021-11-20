import json

from sqlalchemy import Column, Integer, String

from models.__message import Message
from . import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)

    @classmethod
    def get_user(cls, db_session, username: str, create_if_not_exist=True):
        user = db_session.query(cls).filter_by(username=username).first()
        if user:
            return user
        elif create_if_not_exist:
            return cls(username=username)
        else:
            return None

    @classmethod
    def get_all_messages(cls, db_session, username: str):
        user = cls.get_user(db_session=db_session, username=username, create_if_not_exist=False)
        if not user:
            raise ValueError("User doesn't exist")

        messages = json.loads(str(db_session.query(Message).filter_by(receiver_id=user.id).all()))

        return messages

    def __repr__(self):
        return self.username
