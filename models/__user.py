from sqlalchemy import Column, Integer, String

from . import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)

    @classmethod
    def get_or_create(cls, db_session, username: str):
        user = db_session.query(cls).filter_by(username=username).first()
        if user:
            return user
        else:
            return cls(username)
