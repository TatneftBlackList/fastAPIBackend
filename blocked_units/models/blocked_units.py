from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from db.base import Base


class BlockedUnitsModel(Base):
    __tablename__ = 'blocked_units'

    id = Column(Integer, primary_key=True)
    fio = Column(String, nullable=False)
    passport_id = Column(Integer, ForeignKey('passports.id', ondelete='CASCADE'), nullable=False)
    company_id = Column(Integer, ForeignKey('company.id'), nullable=False)
    reason = Column(String, nullable=False)
    date_add_to_list = Column(DateTime, nullable=False, default=datetime.utcnow)

    passports_rel = relationship('PassportsModel',
                                 back_populates='blocked_units_rel')
    company_rel = relationship('CompanyModel', back_populates='blocked_units_rel')
