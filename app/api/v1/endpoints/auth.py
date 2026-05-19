from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse, Token
from app.services.auth_service import AuthService
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()
service = AuthService()

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(__import__('app.models.user', fromlist=['User']).User).filter_by(email=user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return service.register_user(user_data, db)


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = service.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = service.create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}