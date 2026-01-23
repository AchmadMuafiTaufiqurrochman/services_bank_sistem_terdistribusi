from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from app.db.models import Transaction
from app.db.models.transaction_model import TransactionType, TransactionBank
from app.utils.request_middleware import send_to_middleware
from datetime import datetime
from app.repositories.transaction_repository import TransactionRepository
from app.middleware.pin_middleware import validate_pin

class OverbookService:
    def __init__(self, db):
        self.db = db
        self.transaction_repository = TransactionRepository(db)

    async def process_overbook_transaction(self, overbook_data, user):
       
        # 1. Validasi: Cek apakah account number milik customer yang login
        account = await self.transaction_repository.get_account_by_customer_id(user.customer_id)
        
        
        if not account:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Rekening sumber tidak valid atau bukan milik Anda."
            )

        # 2. Validasi PIN
        await validate_pin(overbook_data.PIN, user.customer_id, self.db)

        # 3. Buat Object Transaction & Flush (Dapatkan ID)
        transaction = Transaction(
            transaction_type=TransactionType.TrfOvrbok,
            transaction_bank=TransactionBank.Internal,
            bank_reference=overbook_data.bank_reference,
            source_account_number=account.account_number,
            target_account_number=overbook_data.target_account_number,
            amount=overbook_data.amount,
            currency_code="IDR",
            description=overbook_data.description,
            transaction_date=datetime.now()
        )

        try:
            # Simpan sementara (Flush) untuk mendapatkan transaction_id
            await self.transaction_repository.create_transaction(transaction)
            
            # 4. Kirim ke Middleware (Core) dengan ID yang sudah terbentuk
            payload = jsonable_encoder(overbook_data)
            payload.update({
                "transaction_id": transaction.transaction_id,
                "transaction_type": transaction.transaction_type.value,
                "transaction_bank": transaction.transaction_bank.value,
                "source_account_number": account.account_number
            })
            
            # 5. Kirim ke middleware
            await send_to_middleware(payload, path="/api/v1/transaction/overbook")

            # Update balances
            await self.transaction_repository.update_balance(account.account_number, -overbook_data.amount)
            await self.transaction_repository.update_balance(overbook_data.target_account_number, overbook_data.amount)
            
            # 6. Jika Core sukses, Commit permanen
            await self.db.commit()
            await self.db.refresh(transaction)
            
        except Exception as e:
            # 7. Jika middleware gagal atau ada error lain, Rollback (ID dibatalkan)
            # print(f"DEBUG: Transaction failed. Error: {e}") # Add debug log
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Transaksi gagal: {str(e)}")
            
        return {
            "status": "success",
            "message": "Transaksi berhasil diproses",
            "data": 
            {
                "transaction_bank": transaction.transaction_bank,
                "transaction_type": transaction.transaction_type,
                "target_account_number": transaction.target_account_number,
                "source_account_number": transaction.source_account_number,
                "amount": transaction.amount,
                "description": transaction.description,
                "bank_reference": transaction.bank_reference,
                "currency_code": "IDR",
                "transaction_date": transaction.transaction_date.isoformat()
                }
        }