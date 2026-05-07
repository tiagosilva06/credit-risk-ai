from fastapi import FastAPI
from app.core.database import Base, engine
from app.models import customer, credit_analysis
from app.api.v1.endpoints import customer

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Credit Risk AI",
    description="API for credit risk analysis powered by AI",
    version="1.0.0"
)

app.include_router(customer.router, prefix="/api/v1/endpoints/customer", tags=["Customer"])

@app.get("/health")
def health():
    return {"status": "ok"}