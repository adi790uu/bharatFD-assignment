from fastapi import FastAPI, HTTPException, Request
from contextlib import asynccontextmanager

from fastapi.responses import JSONResponse

from app.exceptions.exception import CustomException
from app.schemas.response import APIResponse, ErrorResponse
from app.routers import faq
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting the server...")
    yield
    print("Closing the server...")


app = FastAPI(title="BharatFD", lifespan=lifespan)


@app.get("/")
async def root():
    api_response = APIResponse(
        success=True,
        message="Server running successfully!",
    )
    return JSONResponse(status_code=200, content=api_response.model_dump())


app.include_router(faq.router, prefix=settings.API_PREFIX)


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exception: Exception):
    if isinstance(exception, CustomException):
        error_response = ErrorResponse(
            success=False, message=exception.message, error=exception.name
        )
        status_code = exception.status_code
    elif isinstance(exception, HTTPException):
        error_response = ErrorResponse(
            success=False, message=exception.detail, error="HTTPException"
        )
        status_code = exception.status_code
    else:
        error_response = ErrorResponse(
            success=False,
            message="An unexpected error occurred.",
            error=str(exception),
        )
        status_code = 500

    return JSONResponse(
        status_code=status_code,
        content=error_response.model_dump(),
    )
