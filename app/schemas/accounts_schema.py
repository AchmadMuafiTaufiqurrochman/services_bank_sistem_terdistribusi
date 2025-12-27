# app/schemas/accounts_schema.py
from pydantic import BaseModel, ConfigDict,Field
from fastapi import Query

class AccountQuery(BaseModel):
    account_number: str | None = Query(
        None,
        min_length=5,
        max_length=30,
        description="Nomor rekening (opsional)"
    )

    model_config = ConfigDict(extra="forbid")  # ⛔ Tidak boleh ada query lain
