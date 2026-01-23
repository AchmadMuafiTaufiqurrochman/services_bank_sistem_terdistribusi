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

class ResponseRegister(BaseModel):
    status: str = Field(..., example="success", description="Status dari operasi registrasi")
    message: str = Field(..., example="Registrasi berhasil", description="Pesan terkait hasil registrasi")

class ResponseLogin(BaseModel):
    status: str = Field(..., example="success", description="Status dari operasi login")
    message: str = Field(..., example="Login berhasil", description="Pesan terkait hasil login")
    data: dict = Field(...,
    example= {
        "status": "success",
        "message": "Login berhasil!",
        "data": {
            "credential": {
        "username": "budisantoso",
        "password": "securepassword123", },
        "customer": {
            "full_name": "Budi Santoso",
            "email": "budi.santoso@example.com",
        },
        "account": {
            "account_number": "1234567890",
            "status": "Active"
        }
        }
    },
     description="Data tambahan terkait login")