# app/routes/v1/auth_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.models import Customer, Login, PortofolioAccount
from app.schemas.auth_schema import RegisterRequest
from passlib.context import CryptContext
import random

router = APIRouter(prefix="/auth", tags=["Auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__ident="2b",)

@router.post("/register")
async def register_user(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    # 1️⃣ Validasi duplikasi data
    for model, field, value in [
        (Customer, Customer.NIK, data.nik),
        (Customer, Customer.email, data.email),
        (Login, Login.username, data.username)
    ]:
        result = await db.execute(select(model).where(field == value))
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{field.key.capitalize()} sudah digunakan!"
            )

    # 2️⃣ Simpan ke tabel customers
    customer = Customer(
        full_name=data.full_name,
        birth_date=data.birth_date,
        address=data.address,
        NIK=data.nik,
        phone_number=data.phone_number,
        email=data.email,
        PIN=int(data.PIN),
        id_portofolio=f"PRT-{random.randint(100000,999999)}"
    )
    db.add(customer)
    await db.flush()  # dapat customer_id

    # 3️⃣ Sanitasi dan hashing password
    password_clean = data.password.strip().encode("utf-8", errors="ignore")

    # Normalisasi — hapus karakter non-ASCII tak terlihat
    password_clean = password_clean.decode("utf-8", errors="ignore")

    # Cek panjang setelah dibersihkan
    if len(password_clean.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password terlalu panjang, maksimal 72 karakter."
        )

    try:
        hashed_password = pwd_context.hash(password_clean)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Gagal memproses password: {str(e)}"
        )

    # 4️⃣ Simpan ke tabel logins
    login = Login(
        username=data.username,
        password_hash=hashed_password,
        customer_id=customer.customer_id
    )
    db.add(login)

    # 5️⃣ Simpan ke tabel portofolio_accounts
    account = PortofolioAccount(
        account_number=f"101{random.randint(1000000,9999999)}",
        customer_id=customer.customer_id
    )
    db.add(account)

    # 6️⃣ Commit dan kembalikan hasil
    customer_id = customer.customer_id
    account_number = account.account_number
    await db.commit()

    return {
        "message": "Registrasi berhasil!",
        "customer_id": customer_id,
        "account_number": account_number
    }