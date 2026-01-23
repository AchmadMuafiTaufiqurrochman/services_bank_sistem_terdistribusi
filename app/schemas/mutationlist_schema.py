from pydantic import BaseModel, Field
from datetime import date

class MutationListQuery(BaseModel):
    start_date: date | None = Field(None, example="2023-01-01", description="Tanggal mulai untuk filter mutasi")
    end_date: date | None = Field(None, example="2023-01-31", description="Tanggal akhir untuk filter mutasi")
    PIN: str = Field(..., min_length=6, max_length=6, example="123456", description="PIN nasabah untuk verifikasi")

class ResponseMutationListSchema(BaseModel):
    status: str = Field(..., example="success", description="Status dari operasi pengambilan mutasi")
    message: str = Field(..., example="Daftar mutasi berhasil diambil", description="Pesan terkait hasil pengambilan mutasi")
    data: list[dict] = Field(..., example=[{
            "account_number": "1234567890",
            "start_date": "2023-01-01",
            "end_date": "2023-01-31"
        }] , description="Daftar mutasi rekening")