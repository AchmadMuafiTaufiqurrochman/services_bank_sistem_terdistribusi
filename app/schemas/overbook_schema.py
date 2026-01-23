# app/schemas/overbook_schema.py
from pydantic import BaseModel, Field
from datetime import date


class OverbookSchema(BaseModel):

    bank_reference: str | None = Field(..., example="Bank Samiun", description="Referensi bank eksternal")
    target_account_number: str = Field(..., example="0987654321", description="Nomor rekening tujuan")
    amount: float = Field(..., gt=0, example=100000, description="Jumlah yang akan ditransfer")
    description: str | None = Field(None, example="Ini Deskripsi", description="Deskripsi transaksi")
    PIN : str = Field(..., example=123456, description="PIN")

class ResponseOverbookSchema(BaseModel):
    status: str = Field(..., example="success", description="Status dari operasi overbook")
    message: str = Field(..., example="Transaksi overbook berhasil diproses", description="Pesan terkait hasil operasi")
    data: dict = Field(..., example={
            "status": "success",
            "message": "Transaksi berhasil diproses",
            "data": 
            {
                "transaction_bank": "Internal",
                "transaction_type": "Overbook",
                "target_account_number": "0987654321",
                "source_account_number": "1234567890",
                "amount": 100000,
                "description": "Ini Deskripsi",
                "bank_reference": "Bank Samiun",
                "currency_code": "IDR",
                "transaction_date": "2024-06-01T12:00:00Z"
                }
        } , description="Data tambahan terkait transaksi overbook")