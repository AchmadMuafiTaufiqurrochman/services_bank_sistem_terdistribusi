# app/routes/v1/auth_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.models import Customer, Login, PortofolioAccount
from app.schemas.auth_schema import RegisterRequest
from passlib.context import CryptContext
import random
from app.middleware.auth_middleware import verify_auth

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__ident="2b",
)

@router.post("/register")
async def register_user(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    # 1️⃣ Cek duplikasi data (NIK, email, username)
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
        PIN=int(data.PIN)
    )
    db.add(customer)
    await db.flush()  # supaya customer_id langsung bisa dipakai

    # 3️⃣ Buat portofolio account yang terhubung ke customer
    account = PortofolioAccount(
        account_number=f"101{random.randint(1000000,9999999)}",
        customer_id=customer.customer_id
    )
    db.add(account)
    await db.flush()

    # 4️⃣ Hash password
    password_clean = data.password.strip().encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")

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

    # 5️⃣ Simpan ke tabel login
    login = Login(
        username=data.username,
        password_hash=hashed_password,
        customer_id=customer.customer_id
    )
    db.add(login)

    # 6️⃣ Commit semua perubahan
    await db.commit()

    # 7️⃣ Return hasil
    return {
        "message": "Registrasi berhasil!",
        # "username_customer": data.username,
        # "password_customer": data.password,
        # "account_number": account.account_number
    }

@router.post("/login")
async def login_user(user: Login = Depends(verify_auth), db: AsyncSession = Depends(get_db)):
    """
    Endpoint login menggunakan middleware autentikasi.
    User mengirimkan header:
    - Authorization-Username
    - Authorization-Password
    """
    # Ambil data customer terkait user login
    result = await db.execute(select(Customer).where(Customer.customer_id == user.customer_id))
    customer = result.scalar_one_or_none()

    if not customer:
        raise HTTPException(status_code=404, detail="Data nasabah tidak ditemukan")

    # Dapat juga kembalikan data portofolio jika ingin
    result = await db.execute(select(PortofolioAccount).where(PortofolioAccount.customer_id == customer.customer_id))
    portofolio = result.scalar_one_or_none()

    return {
        "message": "Login berhasil!",
        "username": user.username,
        "customer": {
            "customer_id": customer.customer_id,
            "full_name": customer.full_name,
            "email": customer.email,
        },
        "account": {
            "account_number": portofolio.account_number if portofolio else None,
            "status": portofolio.status.value if portofolio else None
        }
    }