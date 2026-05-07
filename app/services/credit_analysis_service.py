from sqlalchemy.orm import Session

from app.models.customer import Customer, EmploymentStatus
from app.models.credit_analysis import CreditAnalysis, RiskLevel

class CreditAnalysisService:

    def calculate_score(self, customer: Customer) -> int:
        score = 0

        if customer.age >= 40:
            score += 25
        elif customer.age >= 30:
            score += 15
        elif customer.age >= 25:
            score += 10
        else:
            score += 5

        if customer.monthly_income >= 10000:
            score += 25
        elif customer.monthly_income >= 5000:
            score += 15
        elif customer.monthly_income >= 2000:
            score += 10
        else:
            score += 5
       
        if customer.current_score >= 800:
            score += 25
        elif customer.current_score >= 600:
            score += 15
        elif customer.current_score >= 400:
            score += 8
        else:
            score += 0
       
        debt_ratio = customer.active_debts / customer.monthly_income if customer.monthly_income > 0 else 1
        if debt_ratio <= 0.2:
            score += 15
        elif debt_ratio <= 0.4:
            score += 8
        elif debt_ratio <= 0.6:
            score += 3
        else:
            score -= 10

        if customer.patrimony >= 500000:
            score += 10
        elif customer.patrimony >= 100000:
            score += 7
        elif customer.patrimony >= 20000:
            score += 4

        if customer.employment_status == EmploymentStatus.EMPLOYED:
            score += 10
        elif customer.employment_status == EmploymentStatus.SELF_EMPLOYED:
            score += 5
        else:
            score -= 10

        return max(0, min(score, 100))

    
    def get_risk_level(self, score: int) -> RiskLevel:
        if score >= 75:
            return RiskLevel.LOW
        elif score >= 50:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.HIGH
    

    def create_analysis(self, customer: Customer, requested_amount: float, db: Session) -> CreditAnalysis:
        score = self.calculate_score(customer)
        risk_level = self.get_risk_level(score)

        analysis = CreditAnalysis(
            customer_id=customer.id,
            score=score,
            risk_level=risk_level,
            ai_explanation="Ai analysis will be implemented soon..",
            requested_amount=requested_amount
        )

        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        return analysis