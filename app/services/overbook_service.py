from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from app.db.models import Transaction
from app.repositories.overbook_repository import OverbookRepository
from app.utils.request_middleware import send_to_middleware
from datetime import datetime

class OverbookService:
    def __init__(self, db):
        self.db = db
        self.overbook_repository = OverbookRepository(db)

    async def process_overbook_transaction(self, overbook_data, user):
        # 1. Validasi: Cek apakah account number milik customer yang login
        account = await self.overbook_repository.get_account_by_number_and_customer(
            overbook_data.source_account_number, 
            user.customer_id)
        
        if not account:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Rekening sumber tidak valid atau bukan milik Anda."
            )

        # 2. Validasi PIN
        customer_pin = await self.overbook_repository.get_customer_pin(user.customer_id)
        if customer_pin != overbook_data.PIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="PIN salah."
            )

        # 3. Buat Object Transaction & Flush (Dapatkan ID)
        transaction = Transaction(
            transaction_type=overbook_data.transaction_type,
            transaction_bank=overbook_data.transaction_bank,
            bank_reference=overbook_data.bank_reference,
            source_account_number=overbook_data.source_account_number,
            target_account_number=overbook_data.target_account_number,
            amount=overbook_data.amount,
            currency_code=overbook_data.currency_code,
            description=overbook_data.description,
            transaction_date=datetime.now()
        )

        try:
            # Simpan sementara (Flush) untuk mendapatkan transaction_id
            await self.overbook_repository.create_overbook_transaction(transaction)
            
            # 4. Kirim ke Middleware (Core) dengan ID yang sudah terbentuk
            payload = jsonable_encoder(overbook_data)
            payload["transaction_id"] = transaction.transaction_id  # Sisipkan ID untuk konsistensi
            
            # 5. Kirim ke middleware
            await send_to_middleware(payload, path="/api/v1/transaction/overbook")

            # Update balances
            await self.overbook_repository.update_balance(overbook_data.source_account_number, -overbook_data.amount)
            await self.overbook_repository.update_balance(overbook_data.target_account_number, overbook_data.amount)
            
            # 6. Jika Core sukses, Commit permanen
            await self.db.commit()
            await self.db.refresh(transaction)
            
        except Exception as e:
            # 7. Jika middleware gagal atau ada error lain, Rollback (ID dibatalkan)
            # print(f"DEBUG: Transaction failed. Error: {e}") # Add debug log
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Transaksi gagal: {str(e)}")
            
        return {
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