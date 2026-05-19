from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.models.user import User

from app.core.database import get_db
from app.models.customer import Customer
from app.schemas.credit_analysis import CreditAnalysisRequest, CreditAnalysisResponse
from app.services.credit_analysis_service import CreditAnalysisService

router = APIRouter()
service = CreditAnalysisService()

@router.post("/", response_model=CreditAnalysisResponse)
def create_analysis(request: CreditAnalysisRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    customer = db.query(Customer).filter(Customer.id == request.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return service.create_analysis(customer, request.requested_amount, db)

@router.get("/", response_model=list[CreditAnalysisResponse])
def get_all_analyses(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    from app.models.credit_analysis import CreditAnalysis
    return db.query(CreditAnalysis).all()

@router.get("/{analysis_id}", response_model=CreditAnalysisResponse)
def get_analysis(analysis_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    from app.models.credit_analysis import CreditAnalysis
    analysis = db.query(CreditAnalysis).filter(CreditAnalysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis