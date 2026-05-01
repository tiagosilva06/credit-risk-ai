from pydantic import BaseModel
from datetime import datetime

class CreditAnalysisRequest(BaseModel):
    customer_id: int

class CreditAnalysisResponse(BaseModel):
    id: int
    customer_id: int
    score: int
    risk: str
    ai_explanation: str | None
    created_at: datetime

    class Config:
        from_attributes = True

class CreditAnalysisCreate(BaseModel):
    customer_id: int

