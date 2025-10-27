# app/routes/v1/accounts_router.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.middleware.auth_middleware import verify_auth
from app.services.accounts_service import AccountsService
from app.schemas.accounts_schema import AccountQuery

router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.get("/balance")
async def get_balance(
    params: AccountQuery = Depends(),
    db: AsyncSession = Depends(get_db),
    user = Depends(verify_auth)
):
    service = AccountsService(db)
    return await service.get_balance(user, params.account_number)

@router.get("/detail")
async def get_customer_detail(
    db: AsyncSession = Depends(get_db),
    user = Depends(verify_auth)
):
    service = AccountsService(db)
    return await service.get_customer_detail(user)
