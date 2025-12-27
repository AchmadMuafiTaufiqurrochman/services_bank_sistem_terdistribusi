# app/schemas/auth_schema.py
from pydantic import BaseModel, EmailStr, Field
from datetime import date

class RegisterRequest(BaseModel):
    full_name: str = Field(..., example="Budi Santoso")
    birth_date: date = Field(..., example="1990-04-23")
    address: str = Field(..., example="Jl. Merdeka No. 10, Jakarta")
    nik: str = Field(..., example="3201012304950007")
    phone_number: str = Field(..., example="6281234567890")
    email: EmailStr = Field(..., example="budi.santoso@example.com")
    username: str = Field(..., example="budisantoso")
    password: str = Field(..., example="securepassword123")
    PIN: str = Field(..., example="123456")
