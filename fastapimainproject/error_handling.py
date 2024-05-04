from fastapi.responses import JSONResponse
from fastapi import HTTPException
import logging


def create_response(status_code: int, message: str, data=None, status: str = "success"):
    return JSONResponse(
        status_code=status_code,
        content={
            "statusCode": status_code,
            "message": message,
            "body": data,
            "status": status
        }
    )

# def handle_error(e: Exception):
#     return create_response(500, f"An error occurred: {str(e)}", status="error")

def handle_unsupported_file():
    return create_response(400, "Unsupported file type", status="error")

def handle_error(error):
    """Log the error and return a 500 internal server error response."""
    # Log the error with a stack trace for better diagnosis
    logging.error("An unexpected error occurred", exc_info=True)
    # Depending on the error type, you might want to respond differently
    if isinstance(error, HTTPException):
        return JSONResponse(status_code=error.status_code, content={"detail": error.detail})
    else:
        return JSONResponse(status_code=500, content={"detail": str(error)})

