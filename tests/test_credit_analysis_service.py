import pytest
from unittest.mock import MagicMock
from app.services.credit_analysis_service import CreditAnalysisService
from app.models.customer import Customer, EmploymentStatus

service = CreditAnalysisService()

def make_customer(**kwargs):
    defaults = {
        "age": 30,
        "monthly_income": 5000.0,
        "current_score": 600,
        "active_debts": 500.0,
        "patrimony": 50000.0,
        "employment_status": EmploymentStatus.EMPLOYED
    }
    defaults.update(kwargs)
    customer = MagicMock(spec=Customer)
    for k, v in defaults.items():
        setattr(customer, k, v)
    return customer

def test_score_employed_good_profile():
    customer = make_customer()
    score = service.calculate_score(customer)
    assert score >= 50

def test_score_unemployed_penalized():
    customer = make_customer(employment_status=EmploymentStatus.UNEMPLOYED)
    employed = make_customer(employment_status=EmploymentStatus.EMPLOYED)
    assert service.calculate_score(customer) < service.calculate_score(employed)

def test_score_high_debt_penalized():
    low_debt = make_customer(active_debts=500.0, monthly_income=5000.0)
    high_debt = make_customer(active_debts=4500.0, monthly_income=5000.0)
    assert service.calculate_score(high_debt) < service.calculate_score(low_debt)

def test_score_never_below_zero():
    customer = make_customer(
        age=18,
        monthly_income=1000.0,
        current_score=100,
        active_debts=5000.0,
        patrimony=0.0,
        employment_status=EmploymentStatus.UNEMPLOYED
    )
    assert service.calculate_score(customer) >= 0

def test_score_never_above_100():
    customer = make_customer(
        age=50,
        monthly_income=20000.0,
        current_score=900,
        active_debts=0.0,
        patrimony=1000000.0,
        employment_status=EmploymentStatus.EMPLOYED
    )
    assert service.calculate_score(customer) <= 100

def test_risk_level_low():
    from app.models.credit_analysis import RiskLevel
    assert service.get_risk_level(80) == RiskLevel.LOW

def test_risk_level_medium():
    from app.models.credit_analysis import RiskLevel
    assert service.get_risk_level(60) == RiskLevel.MEDIUM

def test_risk_level_high():
    from app.models.credit_analysis import RiskLevel
    assert service.get_risk_level(30) == RiskLevel.HIGH