from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException, status

async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Custom handler agar HTTPException return { "message": ... } bukan { "detail": ... }
    """
    status_code = getattr(exc, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
    message = getattr(exc, "detail", str(exc))

    return JSONResponse(
        status_code=status_code,
        content={
            "status": "error",
            "message": message,
        },
    )
