from sqlalchemy import Column, Integer, String, UniqueConstraint
from api.database import Base


class DateFact(Base):
    __tablename__ = "date_facts"
    
    __table_args__ = (UniqueConstraint('day', 'month', name="uix_day_month"),)
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    day = Column(Integer, nullable=False)
    month = Column(String(50), nullable=False)
    fact = Column(String(255), nullable=False)
    
    def __repr__(self) -> str:
        return f'<DateFact {self.day}/{self.month}>'

    def __str__(self):
        return self.fact