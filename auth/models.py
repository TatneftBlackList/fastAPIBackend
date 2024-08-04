from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship


from db.base import Base


class AuthModel(Base):
    __tablename__ = 'auth'

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    role = Column(Integer, ForeignKey('roles.id'))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    user_rel = relationship('UserModel', back_populates='auth_rel')
    role_rel = relationship('RolesModel', back_populates='auth_rel')
    request_logs = relationship('UserRequestLogModel', back_populates='user', cascade='all, delete-orphan')
