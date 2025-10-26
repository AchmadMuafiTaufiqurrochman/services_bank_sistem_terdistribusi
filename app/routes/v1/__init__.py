from fastapi import APIRouter
from .auth_router import router as auth_router
from .accounts_router import router as accounts_router

router_v1 = APIRouter()
router_v1.include_router(auth_router)
router_v1.include_router(accounts_router)