import asyncio
from sqlalchemy import text
from app.db.database import engine

async def test_connection():
    print("🔍 Testing database connection...")
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            value = result.scalar()

            if value == 1:
                print("✅ Database connection successful!")
            else:
                print("⚠️ Connected but unexpected result:", value)

    except Exception as e:
        print("❌ Database connection failed!")
        print("Error:", e)

    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_connection())
