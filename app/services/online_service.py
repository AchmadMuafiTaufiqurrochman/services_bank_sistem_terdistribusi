from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from app.db.models import Transaction
from app.utils.request_middleware import send_to_middleware
from datetime import datetime
from app.repositories.transaction_repository import TransactionRepository

class OnlineService:
    def __init__(self, db):
        self.db = db
        self.transaction_repository = TransactionRepository(db)

    async def process_online_transaction(self, online_data, user):
        # 1. Validasi: Cek apakah account number milik customer yang login
        account = await self.transaction_repository.get_account_by_number_and_customer(
            online_data.source_account_number, 
            user.customer_id)
        
        if not account:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Rekening sumber tidak valid atau bukan milik Anda."
            )

        # 2. Validasi PIN
        customer_pin = await self.transaction_repository.get_customer_pin(user.customer_id)
        if customer_pin != online_data.PIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="PIN salah."
            )

        # 3. Buat Object Transaction & Flush (Dapatkan ID)
        transaction = Transaction(
            transaction_type=online_data.transaction_type,
            transaction_bank=online_data.transaction_bank,
            bank_reference=online_data.bank_reference,
            source_account_number=online_data.source_account_number,
            target_account_number=online_data.target_account_number,
            amount=online_data.amount,
            currency_code=online_data.currency_code,
            description=online_data.description,
            transaction_date=datetime.now()
        )

        try:
            # Simpan sementara (Flush) untuk mendapatkan transaction_id
            await self.transaction_repository.create_transaction(transaction)
            
            # 4. Kirim ke Middleware (Core) dengan ID yang sudah terbentuk
            payload = jsonable_encoder(online_data)
            payload["transaction_id"] = transaction.transaction_id  # Sisipkan ID untuk konsistensi
            
            # 5. Kirim ke middleware
            await send_to_middleware(payload, path="/api/v1/transactions/external/execute")

            # Update balances
            await self.transaction_repository.update_balance(online_data.source_account_number, -online_data.amount)
            await self.transaction_repository.update_balance(online_data.target_account_number, online_data.amount)
            
            # 6. Jika Core sukses, Commit permanen
            await self.db.commit()
            await self.db.refresh(transaction)
            
        except Exception as e:
            # 7. Jika middleware gagal atau ada error lain, Rollback (ID dibatalkan)
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
