from sqlalchemy.ext.asyncio import AsyncSession
from app.models.faq import FAQ as FAQModel
from loguru import logger
from app.services import translator as translator_service
from app.schemas.faq import FAQ as FAQSchema


async def create_faq(question: str, answer: str, db: AsyncSession):
    try:
        faq = await FAQModel.create_faq(
            question=question,
            answer=answer,
            db=db,
        )
        faq_dto = FAQSchema(
            id=faq.id,
            answer=faq.answer,
            question=faq.question,
        )
        await translator_service.translate_text(faq=faq_dto, db=db)
        return faq_dto
    except Exception as e:
        logger.error(e)
        raise e
