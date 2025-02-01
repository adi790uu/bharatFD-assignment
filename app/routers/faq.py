from http import HTTPStatus
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from loguru import logger
from app.core.deps import get_db
from app.schemas.request import CreateFAQRequest
from app.schemas.response import APIResponse
from app.services import faq as faq_service


router = APIRouter()


@router.post("/faqs/create")
async def create_faq(request: CreateFAQRequest, db=Depends(get_db)):
    try:
        faq_dto = await faq_service.create_faq(
            question=request.question,
            answer=request.answer,
            db=db,
        )
        api_response = APIResponse(
            success=True,
            message="FAQ created successfully!",
            data=faq_dto.model_dump(),
        )

        return JSONResponse(
            status_code=HTTPStatus.CREATED, content=api_response.model_dump()
        )
    except Exception as e:
        logger.error(e)
        raise e


@router.get("/faqs/")
async def get_faqs(request: Request, db=Depends(get_db)):
    try:
        pass
    except Exception as e:
        logger.error(e)
        raise e
