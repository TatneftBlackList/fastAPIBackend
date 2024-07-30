from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.base import Base


class PassportsModel(Base):
    __tablename__ = 'passports'

    id = Column(Integer, primary_key=True)
    passport_seria = Column(String, unique=True, nullable=False)
    passport_number = Column(String, nullable=False, unique=True)
    old_passport_number = Column(String, nullable=True, unique=True)
    old_passport_seria = Column(String, nullable=True, unique=True)

    blocked_units_rel = relationship('BlockedUnitsModel', back_populates='passports_rel')
