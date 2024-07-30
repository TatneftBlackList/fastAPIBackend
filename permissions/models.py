from sqlalchemy import Column, Integer, String, Enum
from permissions.enums import PermissionEnums
from db.base import Base


class PermissionModel(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True)
    name = Column(Enum(PermissionEnums), nullable=False)
