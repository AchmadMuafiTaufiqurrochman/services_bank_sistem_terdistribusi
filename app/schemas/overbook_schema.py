# app/schemas/overbook_schema.py
from pydantic import BaseModel
from datetime import date


class OverbookSchema(BaseModel):
    transaction_type: str
    transaction_bank: str
    bank_reference: str | None = None
    source_account_number: str
    target_account_number: str
    amount: float
    currency_code: str | None = "IDR"
    description: str | None = None
    transaction_date: date | None = None

