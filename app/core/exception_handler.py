from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
import traceback

async def http_exception_handler(request: Request, exc: Exception):
    """
    Global Exception Handler
    """
    # 1. Handle HTTP Exceptions (Explicit ly raised)
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "error",
                "message": exc.detail,
            },
        )
    
    # 2. Handle Validation Errors (422)
    if isinstance(exc, RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "status": "error",
                "message": exc.errors(), # List of validation errors
            },
        )

    # 3. Handle Other/Unexpected Exceptions (500)
    # Log error untuk debugging di terminal docker logs
    print(f"CRITICAL ERROR: {str(exc)}")
    traceback.print_exc()
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "message": f"Internal Server Error: {str(exc)}",
        },
    )
