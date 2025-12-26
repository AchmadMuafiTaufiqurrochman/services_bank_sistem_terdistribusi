# app/repositories/accounts_repository.py
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.db.models.portofolio_model import PortofolioAccount

class AccountsRepository:
    def __init__(self, db):
        self.db = db

    async def get_account_by_number(self, account_number: str):
        result = await self.db.execute(
            select(PortofolioAccount)
            .options(selectinload(PortofolioAccount.customer))
            .where(PortofolioAccount.account_number == account_number.strip())
        )
        return result.scalar_one_or_none()

    async def get_account_by_customer_id(self, customer_id: int):
        result = await self.db.execute(
            select(PortofolioAccount)
            .options(selectinload(PortofolioAccount.customer))
            .where(PortofolioAccount.customer_id == customer_id)
        )
        return result.scalar_one_or_none()

    async def update_account(self, account: PortofolioAccount):
        self.db.add(account)
        await self.db.commit()
        await self.db.refresh(account)
        return account
