import json

from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Message(Base):
    """Describes a simple message model"""

    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'))
    receiver_id = Column(Integer, ForeignKey('users.id'))
    message = Column(Text, nullable=False)
    subject = Column(String, nullable=False)
    creation_date = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    unread = Column(Boolean, nullable=False, default=True)

    sender = relationship("User", foreign_keys=sender_id)
    receiver = relationship("User", foreign_keys=receiver_id)

    def __repr__(self):
        return json.dumps({
            'sender': str(self.sender),
            'receiver': str(self.receiver),
            'subject': self.subject,
            'message': self.message,
            'created_at': str(self.creation_date),
            'is_unread': self.unread
        })
