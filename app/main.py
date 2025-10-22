from fastapi import FastAPI
from app.routes import router_v1

app = FastAPI(title="Services Backend")
app.include_router(router_v1, prefix="/api/v1")
