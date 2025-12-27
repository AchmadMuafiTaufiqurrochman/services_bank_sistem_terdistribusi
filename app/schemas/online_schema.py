from pydantic import BaseModel, Field
from datetime import date


class OnlineSchema(BaseModel):
    transaction_type: str = Field(..., example="TrfOvrbok", description="Tipe transaksi")
    transaction_bank: str   = Field(..., example="Internal", description="Tipe Transaksi")
    bank_reference: str | None = Field(..., example="Bank Samiun", description="Referensi bank eksternal")
    source_account_number: str = Field(..., example="1234567890", description="Nomor rekening sumber")
    target_account_number: str = Field(..., example="0987654321", description="Nomor rekening tujuan")
    amount: float = Field(..., gt=0, example=100000, description="Jumlah yang akan ditransfer")
    currency_code: str | None = Field("IDR", example="IDR", description="Kode mata uang")
    description: str | None = Field(None, example="Ini Deskripsi", description="Deskripsi transaksi")
    PIN : int = Field(..., example=123456, description="PIN")