# app/db/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
import urllib.parse

encoded_password = urllib.parse.quote_plus(settings.DB_PASSWORD)



# Format URL koneksi database MySQL (async)
DATABASE_URL = (
    f"mysql+aiomysql://{settings.DB_USER}:{encoded_password}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

# Membuat engine asynchronous
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Session factory (tiap request API pakai session sendiri)
async_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

# Base untuk deklarasi model
Base = declarative_base()

# Dependency FastAPI (untuk inject ke route)
async def get_db():
    async with async_session() as session:
        yield session
