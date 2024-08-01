from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from db.base import Base


class CompanyModel(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    blocked_units_rel = relationship('BlockedUnitsModel', back_populates='company_rel')
