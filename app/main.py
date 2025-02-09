from fastapi import FastAPI, HTTPException, Request
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse, JSONResponse
from loguru import logger
from app.core.redis import close_redis_connection
from app.exceptions.exception import CustomException
from app.schemas.response import APIResponse, ErrorResponse
from app.routers import faq
from app.core.config import settings
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Starting the server...")
        yield
        logger.info("Closing the server...")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    finally:
        logger.info("closing Redis connection...")
        await close_redis_connection()


app = FastAPI(title="BharatFD", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    api_response = APIResponse(
        success=True,
        message="Server running successfully!",
    )
    return JSONResponse(status_code=200, content=api_response.model_dump())


@app.get("/user", response_class=HTMLResponse)
async def get_user_page(request: Request):
    return templates.TemplateResponse("user_page.html", {"request": request})


@app.get("/admin", response_class=HTMLResponse)
async def get_admin_page(request: Request):
    return templates.TemplateResponse("admin_page.html", {"request": request})


app.include_router(faq.router, prefix=settings.API_PREFIX)


@app.exception_handler(HTTPException)
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
