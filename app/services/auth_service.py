# app/services/auth_service.py
from fastapi import HTTPException, status
from app.db.models import Customer, Login, PortofolioAccount
from app.repositories.auth_repository import AuthRepository
from passlib.context import CryptContext
import random
from sqlalchemy.future import select


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__ident="2b")

async def register_user(db, data):
    repo = AuthRepository(db)

    # 1️⃣ Cek duplikasi
    for model, field, value in [
        (Customer, Customer.NIK, data.nik),
        (Customer, Customer.email, data.email),
        (Login, Login.username, data.username)
    ]:
        result = await db.execute(select(model).where(field == value))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail=f"{field.key.capitalize()} sudah digunakan!")

    # 2️⃣ Simpan customer
    customer = Customer(
        full_name=data.full_name,
        birth_date=data.birth_date,
        address=data.address,
        NIK=data.nik,
        phone_number=data.phone_number,
        email=data.email,
        PIN=int(data.PIN)
    )
    await repo.create_customer(customer)

    # 3️⃣ Buat portofolio account
    account = PortofolioAccount(
        account_number=f"101{random.randint(1000000,9999999)}",
        customer_id=customer.customer_id
    )
    await repo.create_portofolio(account)

    # 4️⃣ Hash password
    password_clean = data.password.strip().encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")
    if len(password_clean.encode("utf-8")) > 72:
        raise HTTPException(status_code=400, detail="Password terlalu panjang, maksimal 72 karakter.")
    hashed_password = pwd_context.hash(password_clean)

    # 5️⃣ Simpan login
    login = Login(username=data.username, password_hash=hashed_password, customer_id=customer.customer_id)
    await repo.create_login(login)

    await db.commit()
    return {"message": "Registrasi berhasil!"}

async def login_user(user, db):
    """
    Business logic login (menggunakan hasil middleware verify_auth)
    """
    repo = AuthRepository(db)

    # Ambil data customer
    customer = await repo.get_customer_by_id(user.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Data nasabah tidak ditemukan")

    # Ambil data portofolio
    portofolio = await repo.get_portofolio_by_customer_id(customer.customer_id)

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
