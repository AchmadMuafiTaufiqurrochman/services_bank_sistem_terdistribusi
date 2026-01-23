# app/routes/v1/accounts_router.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.middleware.auth_middleware import verify_auth
from app.services.accounts_service import AccountsService
from app.schemas.add_balance_schema import AddBalanceSchema, ResponseBalanceSchema
from app.schemas.mutationlist_schema import MutationListQuery, ResponseMutationListSchema

router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.get("/balance", response_model=ResponseBalanceSchema)
async def get_balance(
    db: AsyncSession = Depends(get_db),
    user = Depends(verify_auth)
):
    service = AccountsService(db)
    return await service.get_balance(user)

@router.get("/detail", response_model=ResponseBalanceSchema)
async def get_customer_detail(
    db: AsyncSession = Depends(get_db),
    user = Depends(verify_auth)
):
    service = AccountsService(db)
    return await service.get_customer_detail(user)

@router.get("/mutationlist", response_model=ResponseMutationListSchema)
async def get_mutation_list(
    params: MutationListQuery = Depends(),
    db: AsyncSession = Depends(get_db),
    user = Depends(verify_auth)
):
    service = AccountsService(db)
    return await service.get_mutation_list(user, params.PIN, params.start_date, params.end_date) 

@router.get("/transactionlist", response_model=ResponseMutationListSchema)
async def get_transaction_list(
    params: MutationListQuery = Depends(),
    db: AsyncSession = Depends(get_db),
    user = Depends(verify_auth)
):
    service = AccountsService(db)
    return await service.get_transaction_list(
        user, 
        params.PIN, 
        params.start_date, 
        params.end_date
    ) 