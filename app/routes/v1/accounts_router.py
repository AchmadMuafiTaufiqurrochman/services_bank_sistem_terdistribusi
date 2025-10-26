# app/routes/v1/accounts_router.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from sqlalchemy.orm import selectinload
from app.db.database import get_db
from app.db.models.customer_model import Customer
from app.db.models.portofolio_model import PortofolioAccount
from app.middleware.auth_middleware import verify_auth

router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.get("/balance")
async def get_balance(
    db: AsyncSession = Depends(get_db),
    user = Depends(verify_auth),
    account_number: str | None = Query(None)
):
    print(f"user.customer_id: {user.customer_id}, account_number param: '{account_number}'")

    if account_number:
        result = await db.execute(
            select(PortofolioAccount)
            .options(selectinload(PortofolioAccount.customer))
            .where(PortofolioAccount.account_number == account_number.strip())
        )
    else:
        result = await db.execute(
            select(PortofolioAccount)
            .options(selectinload(PortofolioAccount.customer))
            .where(PortofolioAccount.customer_id == user.customer_id)
        )

    account = result.scalar_one_or_none()
    print("Akun ditemukan:", account)

    if not account:
        raise HTTPException(status_code=404, detail="Rekening tidak ditemukan untuk pengguna ini")

    return {
        "status": "success",
        "message": "Data saldo berhasil diambil",
        "data": {
            "full_name": account.customer.full_name if account.customer else "Unknown",
            "account_number": account.account_number,
            "currency_code": account.currency_code,
            "balance": float(account.balance),
            "status": account.status.value if account.status else "Unknown",
            "last_updated": account.updated_at.isoformat() if account.updated_at else datetime.utcnow().isoformat()
        }
    }

@router.get("/detail")
async def get_customer_detail(
    db: AsyncSession = Depends(get_db),
    user = Depends(verify_auth)
):
    """
    Ambil data profil nasabah lengkap berdasarkan login aktif.
    Termasuk info rekening utama jika ada.
    """

    # Query rekening nasabah sekaligus join ke customer
    result = await db.execute(
        select(PortofolioAccount)
        .options(selectinload(PortofolioAccount.customer))
        .where(PortofolioAccount.customer_id == user.customer_id)
    )
    account = result.scalar_one_or_none()

    if not account:
        raise HTTPException(status_code=404, detail="Data nasabah tidak ditemukan")

    customer = account.customer

    return {
        "status": "success",
        "message": "Data profil nasabah berhasil diambil",
        "data": {
            "full_name": customer.full_name if customer else "Unknown",
            "birth_date": customer.birth_date.isoformat() if customer and customer.birth_date else None,
            "address": customer.address if customer else None,
            "phone_number": customer.phone_number if customer else None,
            "email": customer.email if customer else None,
            "account_number": account.account_number,
            "currency_code": account.currency_code,
            "balance": float(account.balance),
            "status": account.status.value if account.status else "Unknown",
            "last_updated": account.updated_at.isoformat() if account.updated_at else datetime.utcnow().isoformat()
        }
    }