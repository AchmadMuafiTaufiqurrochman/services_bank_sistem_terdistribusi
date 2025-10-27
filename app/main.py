# app/main.py
from fastapi import FastAPI, HTTPException
from app.routes import router_v1
from app.core.exception_handler import http_exception_handler
from fastapi.exception_handlers import (
    http_exception_handler as default_http_exception_handler
)

app = FastAPI(title="Services Backend")
app.include_router(router_v1, prefix="/api/v1")

app.add_exception_handler(Exception, http_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)