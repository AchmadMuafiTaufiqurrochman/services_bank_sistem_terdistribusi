# app/schemas/migration.py
import asyncio
from app.db.database import engine, Base
from app.db.models import (
    customer_model,
    login_model,
    portofolio_model,
    transaction_model,
    mutation_model
)

async def migrate():
    print("🚀 Starting database migration...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("✅ Migration completed successfully!")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(migrate())
