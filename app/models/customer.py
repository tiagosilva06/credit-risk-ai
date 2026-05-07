from sqlalchemy import Column, Integer, String, Float, Enum
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base

class EmploymentStatus(enum.Enum):
    EMPLOYED = "employed"
    SELF_EMPLOYED = "self_employed"
    UNEMPLOYED = "unemployed"

class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    monthly_income = Column(Float, nullable=False)
    current_score = Column(Integer, nullable=False)
    active_debts = Column(Float, default=0.0)
    patrimony = Column(Float, default=0.0)
    employment_status = Column(Enum(EmploymentStatus), nullable=False)

    analyses = relationship("CreditAnalysis", back_populates="customer")