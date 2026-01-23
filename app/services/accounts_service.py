# app/services/accounts_service.py
from datetime import datetime
from decimal import Decimal
from fastapi import HTTPException, status
from app.repositories.accounts_repository import AccountsRepository
from app.repositories.transaction_repository import TransactionRepository
from app.utils.request_middleware import send_to_middleware
from app.middleware.pin_middleware import validate_pin

class AccountsService:
    def __init__(self, db):
        self.db = db
        self.repo = AccountsRepository(db)
        self.transaction_repo = TransactionRepository(db)

    async def get_balance(self, user):

        account = await self.repo.get_account_by_customer_id(user.customer_id)

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
    
    async def add_balance(self, user, pin: str, amount: float):
        
        # print(f"DEBUG: User object: {user}")
        # print(f"DEBUG: Customer ID: {user.customer_id}")
        account = await self.repo.get_account_by_customer_id(user.customer_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rekening tidak ditemukan"
            )
        
        await validate_pin(pin, user.customer_id, self.db)

        payload = {
            "account_number": account.account_number,
            "amount": amount,
        }

        await send_to_middleware(payload, path="/api/v1/portofolio/balance/deposit")

        account.balance += Decimal(amount)
        await self.repo.update_account(account)

        return {
            "status": "success",
            "message": "Saldo berhasil ditambahkan",
            "data": {
                "account_number": account.account_number,
                "balance": account.balance,
                "currency_code": account.currency_code
            }
        }

    async def get_mutation_list(self, user, pin: str, start_date=None, end_date=None):

        account = await self.repo.get_account_by_customer_id(user.customer_id)

        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rekening tidak ditemukan untuk pengguna ini"
            )

        await validate_pin(pin, user.customer_id, self.db)

        payload = {
            "account_number": account.account_number,
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None
        }

        # Mengirim request ke middleware untuk mendapatkan data mutasi
        middleware_response = await send_to_middleware(payload, path="/api/v1/transaction/mutationlist")

        data = middleware_response if isinstance(middleware_response, list) else middleware_response.get("data", [])

        return {
            "status": "success",
            "message": "Daftar mutasi berhasil diambil",
            "data": data
        }

    async def get_transaction_list(self, user, pin: str, start_date=None, end_date=None):

        account = await self.repo.get_account_by_customer_id(user.customer_id)

        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rekening tidak ditemukan untuk pengguna ini"
            )

        await validate_pin(pin, user.customer_id, self.db)
        
        try:
            # Karena start_date dan end_date adalah objek date (bukan string), kita tidak bisa melakukan .strip()
            # Kita hanya convert ke datetime
            if start_date and not isinstance(start_date, datetime):
                 start_date = datetime.combine(start_date, datetime.min.time())
            
            if end_date and not isinstance(end_date, datetime):
                 end_date = datetime.combine(end_date, datetime.max.time())
                 
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid date format: {str(e)}")

        transactions = await self.transaction_repo.get_transactions(
            account.account_number, 
            start_date, 
            end_date
        )

        data = []
        for trx in transactions:
            data.append({
                "transaction_id": trx.transaction_id,
                "type": trx.transaction_type.value,
                "bank": trx.transaction_bank.value,
                "amount": float(trx.amount),
                "currency": trx.currency_code,
                "source_account": trx.source_account_number,
                "target_account": trx.target_account_number,
                "description": trx.description,
                "date": trx.transaction_date.isoformat(),
            })

        return {
            "status": "success",
            "message": "Daftar transaksi berhasil diambil",
            "data": data
        }

    async def withdraw_balance(self, user, pin: str, amount: float):
        account = await self.repo.get_account_by_customer_id(user.customer_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rekening tidak ditemukan"
            )

        if account.balance < Decimal(amount):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Saldo tidak mencukupi untuk penarikan"
            )
        await validate_pin(pin, user.customer_id, self.db)

        payload = {
            "account_number": account.account_number,
            "amount": amount
        }

        await send_to_middleware(payload, path="/api/v1/portofolio/balance/withdraw")

        account.balance -= Decimal(amount)
        await self.repo.update_account(account)

        return {
            "status": "success",
            "message": "Saldo berhasil ditarik",
            "data": {
                "account_number": account.account_number,
                "balance": account.balance,
                "currency_code": account.currency_code
            }
        }