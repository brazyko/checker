from datetime import datetime
from sqlalchemy import Integer, Column, DateTime, DECIMAL, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True, default=None, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    products = Column(JSONB, default=dict)
    payment_type = Column(String, nullable=False)
    payment_amount = Column(DECIMAL, nullable=False)
    total = Column(DECIMAL, nullable=False)
    rest = Column(DECIMAL, nullable=False)
