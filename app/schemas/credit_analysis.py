from pydantic import BaseModel
from datetime import datetime
from app.models.credit_analysis import RiskLevel

class CreditAnalysisRequest(BaseModel):
    customer_id: int
    requested_amount: float

class CreditAnalysisResponse(BaseModel):
    id: int
    customer_id: int
    score: int
    risk_level: RiskLevel
    ai_explanation: str | None
    created_at: datetime

    class Config:
        from_attributes = True

