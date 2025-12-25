from sqlalchemy.future import select
from app.db.models import Transaction, PortofolioAccount

class OverbookRepository:
    def __init__(self, db):
        self.db = db
        
    async def create_overbook_transaction(self, transaction: Transaction):
        self.db.add(transaction)
        await self.db.flush()
        return transaction

    async def get_account_by_number_and_customer(self, account_number: str, customer_id: int):
        result = await self.db.execute(
            select(PortofolioAccount).where(
                PortofolioAccount.account_number == account_number,
                PortofolioAccount.customer_id == customer_id
            )
        )
        return result.scalar_one_or_none()