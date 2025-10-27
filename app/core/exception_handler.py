from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException

async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Custom handler agar HTTPException return { "message": ... } bukan { "detail": ... }
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,  # ambil dari field bawaan HTTPException
        },
    )
