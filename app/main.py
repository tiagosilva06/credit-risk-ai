from app.api.v1.endpoints import auth
from app.models import user as user_model
from fastapi import FastAPI
from app.core.database import Base, engine
from app.models import customer, credit_analysis as credit_analysis_model
from app.api.v1.endpoints import customer, credit_analysis

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Credit Risk AI",
    description="API for credit risk analysis powered by AI",
    version="1.0.0"
)

app.include_router(customer.router, prefix="/api/v1//customer", tags=["Customer"])
app.include_router(credit_analysis.router, prefix="/api/v1/credit_analysis", tags=["Credit Analysis"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])


@app.get("/health")
def health():
    return {"status": "ok"}