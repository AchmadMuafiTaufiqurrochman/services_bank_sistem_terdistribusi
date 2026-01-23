from pydantic import BaseModel, Field

class AddBalanceSchema(BaseModel):
    amount: float = Field(..., gt=0, example=100000, description="Jumlah saldo yang ingin ditambahkan")
    PIN : str = Field(..., min_length=6, max_length=6, example="123456", description="PIN nasabah untuk verifikasi")

class ResponseBalanceSchema(BaseModel):
    status: str = Field(..., example="success", description="Status dari operasi penambahan saldo")
    message: str = Field(..., example="Saldo berhasil ditambahkan", description="Pesan terkait hasil operasi")
    data: dict = Field(...,
    example={
                "full_name": "Gondes",
                "account_number": "1234567890",
                "currency_code": "IDR",
                "balance": 1000000.0,
                "status": "Active",
                "last_updated": "2024-06-01T12:00:00Z"
            },
    description="Data tambahan terkait penambahan saldo")