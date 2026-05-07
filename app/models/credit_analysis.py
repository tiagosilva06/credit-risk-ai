from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum

from app.core.database import Base


class RiskLevel(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class CreditAnalysis(Base):
    __tablename__ = "credit_analysis" 

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)

    score = Column(Integer, nullable=False)
    requested_amount = Column(Float, nullable=False)
    risk_level = Column(Enum(RiskLevel), nullable=False)
    ai_explanation = Column(String, nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    customer = relationship("Customer", back_populates="analyses")
