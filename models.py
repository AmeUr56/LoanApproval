from pydantic import BaseModel

class AppSubmittion(BaseModel):
    application_id: str
    income: float
    loan_amount: float

class AppStatus(BaseModel):
    state: str
    risk_score: int
    decision: str | None