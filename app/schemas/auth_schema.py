from pydantic import BaseModel, EmailStr, Field, constr
from datetime import date

PasswordStr = constr(max_length=72)
class RegisterRequest(BaseModel):
    full_name: str = Field(..., example="Budi Santoso")
    birth_date: date
    address: str
    nik: str = Field(..., example="3201012304950007")
    phone_number: str
    email: EmailStr
    username: str
    password: constr(max_length=72)
    PIN: constr(min_length=6, max_length=6)
