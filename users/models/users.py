from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    job_number = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    user_permissions_rel = relationship('UserPermissionModel',
                                        back_populates='user_rel',
                                        passive_deletes=True,
                                        cascade='all, delete-orphan')
    auth_rel = relationship('AuthModel',
                            uselist=False,
                            back_populates='user_rel',
                            passive_deletes=True,
                            cascade='all, delete-orphan')

