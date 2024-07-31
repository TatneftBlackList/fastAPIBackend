from sqlalchemy import Integer, String, Boolean, Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base


class UserPermissionModel(Base):
    __tablename__ = 'user_permissions'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    permission_id = Column(Integer, ForeignKey('permissions.id'), primary_key=True)


    user_rel = relationship('UserModel', back_populates='user_permissions_rel')
    permission_rel = relationship('PermissionModel', back_populates='user_permissions_rel')
