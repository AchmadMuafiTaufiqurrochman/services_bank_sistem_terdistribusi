# app/routes/v1/auth_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.auth_schema import RegisterRequest
from app.services.auth_service import register_user, login_user
from app.middleware.auth_middleware import verify_auth

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    return await register_user(db, data)

@router.post("/login")
async def login(user = Depends(verify_auth), db: AsyncSession = Depends(get_db)):
    return await login_user(user, db)
