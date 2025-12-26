from pydantic import BaseModel, Field

class AddBalanceSchema(BaseModel):
    amount: float = Field(..., gt=0, description="Jumlah saldo yang ingin ditambahkan")
