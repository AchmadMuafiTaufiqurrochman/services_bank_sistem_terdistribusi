from fastapi import Header, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext

from app.db.database import get_db
from app.db.models.login_model import Login

# Konfigurasi hashing (gunakan bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def verify_auth(
    authorization_username: str = Header(..., alias="Authorization-Username"),
    authorization_password: str = Header(..., alias="Authorization-Password"),
    db: AsyncSession = Depends(get_db)
):
    """
    Middleware autentikasi yang memverifikasi username & password dari header
    berdasarkan data di tabel logins.
    """
    # Cari username di tabel logins
    query = select(Login).where(Login.username == authorization_username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="Username not found")

    # Verifikasi password (hash bcrypt)
    if not pwd_context.verify(authorization_password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid password")

    # Jika lolos, kembalikan data pengguna (bisa diakses di route)
    return user
