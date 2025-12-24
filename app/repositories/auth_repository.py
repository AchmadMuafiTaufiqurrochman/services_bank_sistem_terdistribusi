# app/repositories/auth_repository.py
from sqlalchemy.future import select
from app.db.models import Customer, Login, PortofolioAccount

class AuthRepository:
    def __init__(self, db):
        self.db = db

    async def get_customer_by_field(self, field, value):
        result = await self.db.execute(select(Customer).where(field == value))
        return result.scalar_one_or_none()

    async def get_login_by_field(self, field, value):
        result = await self.db.execute(select(Login).where(field == value))
        return result.scalar_one_or_none()

    async def get_customer_by_id(self, customer_id: int):
        result = await self.db.execute(select(Customer).where(Customer.customer_id == customer_id))
        return result.scalar_one_or_none()

    async def get_portofolio_by_customer_id(self, customer_id: int):
        result = await self.db.execute(select(PortofolioAccount).where(PortofolioAccount.customer_id == customer_id))
        return result.scalar_one_or_none()

    async def create_customer(self, customer):
        self.db.add(customer)
        await self.db.flush()
        return customer

    async def create_portofolio(self, portofolio):
        self.db.add(portofolio)
        await self.db.flush()
        return portofolio

    async def create_login(self, login):
        self.db.add(login)
        return login
