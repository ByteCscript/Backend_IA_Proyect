from pydantic import BaseModel
from datetime import date, datetime

class ProductivityOut(BaseModel):
    id: int
    user_id: int
    date: date
    value: float

    class Config:
        orm_mode = True

class SaleOut(BaseModel):
    id: int
    user_id: int
    date: date
    amount: float

    class Config:
        orm_mode = True

class ReportOut(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    type: str

    class Config:
        orm_mode = True
