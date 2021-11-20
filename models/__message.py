from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from . import Base
from .__user import User


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'))
    receiver_id = Column(Integer, ForeignKey('users.id'))
    message = Column(Text, nullable=False)
    subject = Column(String, nullable=False)
    creation_date = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    sender = relationship("User", back_populates="messages")
    receiver = relationship("User", back_populates="messages")


User.messages = relationship("Message", back_populate="user")
