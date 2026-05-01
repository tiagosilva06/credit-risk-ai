from pydantic import BaseModel
from app.models.customer import EmploymentStatus
from datetime import datetime



class CustomerRequest(BaseModel):
    name: str 
    email: str
    age: int 
    monthly_income: float 
    current_score: int 
    active_debts: float  
    patrimony: float 
    employment_status: EmploymentStatus

class CustomerResponse(BaseModel):
    id: int
    name: str 
    email: str
    age: int 
    monthly_income: float 
    current_score: int 
    active_debts: float  
    patrimony: float 
    employment_status: EmploymentStatus

class Config:
    from_attributes = True