from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def register_user(self, user_data: UserCreate, db: Session) -> User:
        hashed = self.hash_password(user_data.password)
        user = User(name=user_data.name, email=user_data.email, hashed_password=hashed)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def authenticate_user(self, email: str, password: str, db: Session) -> User | None:
        user = db.query(User).filter(User.email == email).first()
        if not user or not self.verify_password(password, user.hashed_password):
            return None
        return user