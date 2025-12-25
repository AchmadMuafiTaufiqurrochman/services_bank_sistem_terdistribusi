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

        # 2. Buat Object Transaction & Flush (Dapatkan ID)
        transaction = Transaction(
            transaction_type=overbook_data.transaction_type,
            transaction_bank=overbook_data.transaction_bank,
            bank_reference=overbook_data.bank_reference,
            source_account_number=overbook_data.source_account_number,
            target_account_number=overbook_data.target_account_number,
            amount=overbook_data.amount,
            currency_code=overbook_data.currency_code,
            description=overbook_data.description,
            transaction_date=overbook_data.transaction_date or datetime.now()
        )

        try:
            # Simpan sementara (Flush) untuk mendapatkan transaction_id
            await self.overbook_repository.create_overbook_transaction(transaction)
            
            # 3. Kirim ke Middleware (Core) dengan ID yang sudah terbentuk
            payload = jsonable_encoder(overbook_data)
            payload["transaction_id"] = transaction.transaction_id  # Sisipkan ID untuk konsistensi
            
            # Kirim ke middleware
            await send_to_middleware(payload, path="/api/v1/transaction/overbook")
            
            # 4. Jika Core sukses, Commit permanen
            await self.db.commit()
            await self.db.refresh(transaction)
            
        except Exception as e:
            # Jika middleware gagal atau ada error lain, Rollback (ID dibatalkan)
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Transaksi gagal: {str(e)}")
            
        return {
            "message": "Transaksi berhasil diproses",
            "data": transaction
        }