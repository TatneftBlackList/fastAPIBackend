from sqlalchemy import Integer, Column, Enum
from sqlalchemy.orm import relationship

from roles.enums import RolesEnum

from db.base import Base


class RolesModel(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(Enum(RolesEnum), nullable=False, unique=True)

    auth_rel = relationship('AuthModel', back_populates='role_rel')
