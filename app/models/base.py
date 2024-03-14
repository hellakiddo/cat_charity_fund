from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, CheckConstraint

from app.core.db import Base

REPRESENTATION = (
    'Сумма: {full_amount}\n'
    'Дата создания: {create_date}\n'
    'Cтатус: {fully_invested}\n'
    'Дата закрытия: {close_date}\n'
)

class PreBaseDonationCharity(Base):
    __abstract__ = True
    __table_args__ = (
        CheckConstraint('invested_amount >= 0'),
        CheckConstraint('full_amount > 0'),
        CheckConstraint('full_amount >= invested_amount'),
    )
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    def __repr__(self):
        return REPRESENTATION.format(
            full_amount=self.full_amount,
            create_date=self.create_date,
            fully_invested=self.fully_invested,
            close_date=self.close_date if self.close_date else ' --- '
        )
