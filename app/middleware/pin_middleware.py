from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.transaction_repository import TransactionRepository

async def validate_pin(input_pin: int, customer_id: int, db: AsyncSession):
    """
    Validasi PIN customer.
    Mengambil PIN dari database menggunakan TransactionRepository dan membandingkannya dengan input_pin.
    Jika tidak cocok, raise HTTPException 403.
    """
    transaction_repository = TransactionRepository(db)
    customer_pin = await transaction_repository.get_customer_pin(customer_id)
    
    # Pastikan perbandingan dilakukan dengan tipe data yang sama
    if str(customer_pin) != str(input_pin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="PIN salah."
        )
