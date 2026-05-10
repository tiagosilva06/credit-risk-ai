from groq import Groq
from app.core.config import settings
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
        

    
    def generate_ai_analysis(self, customer: Customer, score: int, risk_level: RiskLevel):
        prompt = f"""
        You are a credit analyst. Based on the following customer data, provide a professional credit analysis in Portuguese (Brazil).

        Customer Data:
        - Name: {customer.name}
        - Age: {customer.age}
        - Monthly Income: R$ {customer.monthly_income:,.2f}
        - Current Credit Score: {customer.current_score}
        - Active Debts: R$ {customer.active_debts:,.2f}
        - Patrimony: R$ {customer.patrimony:,.2f}
        - Employment Status: {customer.employment_status.value}

        Calculated Risk Score: {score}/100
        Risk Level: {risk_level.value}
    
        Provide a clear and objective analysis in 3 paragraphs:
        1. Customer financial profile summary
        2. Main risk factors identified
        3. Credit recommendation
        """

        client = Groq(api_key=settings.GROQ_API_KEY)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        return response.choices[0].message.content
    

    def create_analysis(self, customer: Customer, requested_amount: float, db: Session) -> CreditAnalysis:
        score = self.calculate_score(customer)
        risk_level = self.get_risk_level(score)
        ai_explanation = self.generate_ai_analysis(customer, score, risk_level)

        analysis = CreditAnalysis(
            customer_id=customer.id,
            score=score,
            risk_level=risk_level,
            ai_explanation=ai_explanation,
            requested_amount=requested_amount
        )

        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        return analysis