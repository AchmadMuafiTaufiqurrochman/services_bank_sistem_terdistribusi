from sqlalchemy.future import select
from sqlalchemy import update, or_
from app.db.models import Transaction, PortofolioAccount, Customer
from decimal import Decimal

class TransactionRepository:
    def __init__(self, db):
        self.db = db
        
    async def create_transaction(self, transaction: Transaction):
        self.db.add(transaction)
        await self.db.flush()
        return transaction

    async def update_balance(self, account_number: str, amount: float):
        stmt = (
            update(PortofolioAccount)
            .where(PortofolioAccount.account_number == account_number)
            .values(balance=PortofolioAccount.balance + Decimal(amount))
            .execution_options(synchronize_session=False)
        )
        await self.db.execute(stmt)

    async def get_account_by_number_and_customer(self, account_number: str, customer_id: int):
        result = await self.db.execute(
            select(PortofolioAccount).where(
                PortofolioAccount.account_number == account_number,
                PortofolioAccount.customer_id == customer_id
            )
        )
        return result.scalar_one_or_none()
    
    async def get_account_by_customer_id(self, customer_id: int):
        result = await self.db.execute(
            select(PortofolioAccount)
            .where(PortofolioAccount.customer_id == customer_id)
        )
        return result.scalar_one_or_none()

    async def get_customer_pin(self, customer_id: int):
        result = await self.db.execute(
            select(Customer.PIN).where(Customer.customer_id == customer_id)
        )
        return result.scalar_one_or_none()

    async def get_transactions(self, account_number: str, start_date=None, end_date=None):
        query = select(Transaction).where(Transaction.source_account_number == account_number)
        
        if start_date:
            query = query.where(Transaction.transaction_date >= start_date)
        if end_date:
            query = query.where(Transaction.transaction_date <= end_date)
            
        query = query.order_by(Transaction.transaction_date.desc())
        
        result = await self.db.execute(query)
        return result.scalars().all()
