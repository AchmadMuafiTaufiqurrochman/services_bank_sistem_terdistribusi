# app/routes/v1/transaction_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.middleware.auth_middleware import verify_auth
from app.schemas.overbook_schema import OverbookSchema
from app.services.overbook_service import OverbookService

router = APIRouter(prefix="/transaction", tags=["Transaction"])

@router.post("/overbook")
async def overbook_transaction(overbook_data: OverbookSchema, user = Depends(verify_auth), db: AsyncSession = Depends(get_db)):
    # Placeholder for overbook transaction logic
    return await OverbookService(db).process_overbook_transaction(overbook_data, user)

@router.post("/online")
async def online_transaction(user = Depends(verify_auth), db: AsyncSession = Depends(get_db)):
    # Placeholder for online transaction logic
    return {"message": "Online transaction processed"}