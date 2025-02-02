from http import HTTPStatus
import json
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from loguru import logger
from app.core import redis
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
            language=None,
            db=db,
        )

        cache_key = f"faqs:{request.language}"
        cached_faqs = await redis.get_redis_with_retry(cache_key)

        if cached_faqs:
            faqs = json.loads(cached_faqs)
            faqs.append(faq_dto.model_dump())
            await redis.set_redis_with_retry(
                cache_key, json.dumps(faqs), expiration=3600
            )

        api_response = APIResponse(
            success=True,
            message="FAQ created successfully!",
        )

        return JSONResponse(
            status_code=HTTPStatus.CREATED, content=api_response.model_dump()
        )
    except Exception as e:
        logger.error(e)
        raise e


@router.get("/faqs/")
async def get_faqs(lang: str = "en", db=Depends(get_db)):
    try:
        logger.info(lang)
        cache_key = f"faqs:{lang}"
        cached_faqs = await redis.get_redis_with_retry(cache_key)

        if cached_faqs:
            faqs = json.loads(cached_faqs)
        else:
            faqs = await faq_service.get_all_faqs_by_language(db=db, lang=lang)
            await redis.set_redis_with_retry(
                cache_key, json.dumps(faqs), expiration=3600
            )

        api_response = APIResponse(
            success=True,
            message="Faqs fetched successfully!",
            data={
                "faqs": faqs,
            },
        )
        return JSONResponse(
            status_code=HTTPStatus.OK, content=api_response.model_dump()
        )
    except Exception as e:
        logger.error(e)
        raise e


@router.delete("/faqs/delete")
async def delete_faq(faq_id: int, db=Depends(get_db)):
    try:
        print(faq_id)
        await faq_service.delete_faq(db=db, faq_id=faq_id)
        await redis.flush_all_keys()
        api_response = APIResponse(
            success=True,
            message="Faq deleted successfully!",
        )
        return JSONResponse(
            status_code=HTTPStatus.OK, content=api_response.model_dump()
        )
    except Exception as e:
        logger.error(e)
        raise e
