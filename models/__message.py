from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, func, ForeignKey,
from sqlalchemy.orm import relationship
from . import Base


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'))
    receiver_id = Column(Integer, ForeignKey('users.id'))
    message = Column(Text, nullable=False)
    subject = Column(String, nullable=False)
    creation_date = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    unread = Column(Boolean, nullable=False, server_default=True)

    sender = relationship("User", foreign_keys=sender_id)
    receiver = relationship("User", foreign_keys=receiver_id)
