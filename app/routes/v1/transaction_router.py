# app/routes/v1/transaction_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.middleware.auth_middleware import verify_auth
from app.schemas.overbook_schema import OverbookSchema, ResponseOverbookSchema
from app.schemas.online_schema import OnlineSchema, ResponseOnlineSchema
from app.schemas.add_balance_schema import AddBalanceSchema, ResponseBalanceSchema
from app.services.overbook_service import OverbookService
from app.services.online_service import OnlineService   
from app.services.accounts_service import AccountsService

router = APIRouter(prefix="/transaction", tags=["Transaction"])

@router.post("/overbook" , response_model=ResponseOverbookSchema)
async def overbook_transaction(overbook_data: OverbookSchema, user = Depends(verify_auth), db: AsyncSession = Depends(get_db)):
    # Placeholder for overbook transaction logic
    return await OverbookService(db).process_overbook_transaction(overbook_data, user)

@router.post("/online", response_model=ResponseOnlineSchema)
async def online_transaction(online_data: OnlineSchema, user = Depends(verify_auth), db: AsyncSession = Depends(get_db)):
    # Placeholder for online transaction logic
    return await OnlineService(db).process_online_transaction(online_data, user)

@router.post("/balance/deposit", response_model=ResponseBalanceSchema)
async def add_balance(
    payload: AddBalanceSchema,
    db: AsyncSession = Depends(get_db),
    user = Depends(verify_auth)
):
    service = AccountsService(db)
    return await service.add_balance(user, payload.PIN, payload.amount)

@router.post("/balance/withdraw", response_model=ResponseBalanceSchema)
async def withdraw_balance(
    payload: AddBalanceSchema,
    db: AsyncSession = Depends(get_db),
    user = Depends(verify_auth)
):
    service = AccountsService(db)
    return await service.withdraw_balance(user, payload.PIN, payload.amount)