from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.core.database import Base


class CreditAnalysis():
    __tablename__ = "credit_analysis" 

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)

    score = Column(Integer, nullable=False)
    risk = Column(String, nullable=False)
    ai_explanation = Column(String, nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    customer = relationship("Customer", back_populates="analyses")