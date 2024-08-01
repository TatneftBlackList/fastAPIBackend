from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base


class UserRequestLogModel(Base):
    __tablename__ = 'user_request_logs'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('auth.id', ondelete='CASCADE'), nullable=False)
    path = Column(String, nullable=False)
    method = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    response_status = Column(Integer, nullable=False)

    user = relationship('AuthModel', back_populates='request_logs')
