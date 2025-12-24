# app/schemas/auth_schema.py
from pydantic import BaseModel, EmailStr, Field
from datetime import date

class RegisterRequest(BaseModel):
    full_name: str = Field(..., example="Budi Santoso")
    birth_date: date
    address: str
    nik: str = Field(..., example="3201012304950007")
    phone_number: str
    email: EmailStr
    username: str
    password: str
    PIN: str
