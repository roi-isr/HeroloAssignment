import json

from sqlalchemy import Column, Integer, String, or_

from models.__message import Message
from utils import hash, safe_pwd_cmp
from . import Base


class User(Base):
    """Describes a messaging user model"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, default=hash.hash_password("password"))

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
    def get_all_messages(cls, db_session, username: str, unread_only=False):
        user = cls.__find_user(db_session, username)

        if unread_only:
            messages = json.loads(str(db_session.query(Message).filter_by(receiver_id=user.id, unread=True).all()))
        else:
            messages = json.loads(str(db_session.query(Message).filter_by(receiver_id=user.id).all()))

        return messages

    @classmethod
    def read_message(cls, db_session, username: str):
        user = cls.__find_user(db_session, username)
        unread_message = db_session.query(Message).filter_by(receiver_id=user.id, unread=True).first()
        if not unread_message:
            raise ValueError(f"No unread messages found for {username}")
        unread_message.unread = False
        db_session.merge(unread_message)
        db_session.commit()
        return json.loads(str(unread_message))

    @classmethod
    def delete_message(cls, db_session, username: str):
        user = cls.__find_user(db_session, username)
        msg = db_session.query(Message).filter(
            or_(Message.sender_id == user.id, Message.receiver_id == user.id)).first()

        if not msg:
            raise ValueError(f"No messages found for {username} as a sender or a receiver")

        db_session.delete(msg)
        db_session.commit()

    @classmethod
    def verify_user(cls, db_session, username: str, password: str):
        try:
            user = cls.__find_user(db_session, username)
        except ValueError:
            return False

        hashed_password = hash.hash_password(password)

        if user and safe_pwd_cmp.safe_pwd_cmp(hashed_password, user.password):
            return user
        return None

    @classmethod
    def __find_user(cls, db_session, username: str):
        user = cls.get_user(db_session=db_session, username=username, create_if_not_exist=False)

        if not user:
            raise ValueError(f"The user specified ({username}) doesn't exist")
        return user

    def __repr__(self):
        return str(self.username)
