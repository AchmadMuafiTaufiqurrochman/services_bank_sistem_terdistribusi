# app/routes/v1/transaction_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.middleware.auth_middleware import verify_auth
from app.schemas.overbook_schema import OverbookSchema
from app.schemas.online_schema import OnlineSchema
from app.services.overbook_service import OverbookService
from app.services.online_service import OnlineService   

router = APIRouter(prefix="/transaction", tags=["Transaction"])

@router.post("/overbook")
async def overbook_transaction(overbook_data: OverbookSchema, user = Depends(verify_auth), db: AsyncSession = Depends(get_db)):
    # Placeholder for overbook transaction logic
    return await OverbookService(db).process_overbook_transaction(overbook_data, user)

@router.post("/online")
async def online_transaction(online_data: OnlineSchema, user = Depends(verify_auth), db: AsyncSession = Depends(get_db)):
    # Placeholder for online transaction logic
    return await OnlineService(db).process_online_transaction(online_data, user)