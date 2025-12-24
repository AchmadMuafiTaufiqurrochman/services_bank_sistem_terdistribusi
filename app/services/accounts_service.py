# app/services/accounts_service.py
from datetime import datetime
from fastapi import HTTPException, status
from app.repositories.accounts_repository import AccountsRepository

class AccountsService:
    def __init__(self, db):
        self.repo = AccountsRepository(db)

    async def get_balance(self, user, account_number: str | None = None):
        if account_number:
            account = await self.repo.get_account_by_number(account_number)


        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rekening tidak ditemukan untuk pengguna ini"
            )

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

    async def get_customer_detail(self, user):
        account = await self.repo.get_account_by_customer_id(user.customer_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Data nasabah tidak ditemukan"
            )

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
