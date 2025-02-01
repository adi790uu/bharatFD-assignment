from googletrans import Translator
from app.schemas.faq import FAQ as FAQSchema
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from app.models.faq import FAQTranslation as FAQTranslationModels

translator = Translator()
SUPPORTED_LANGUAGES = ["en", "hi", "bn"]


async def translate_text(faq: FAQSchema, db: AsyncSession):
    try:
        for lang in SUPPORTED_LANGUAGES:
            translated_question = await translator.translate(
                text=faq.question,
                dest=lang,
            )
            translated_answer = await translator.translate(
                text=faq.answer,
                dest=lang,
            )

            await FAQTranslationModels.add_faq_translation(
                db=db,
                translated_question=translated_question.text,
                translated_answer=translated_answer.text,
                faq_id=faq.id,
                lang=lang,
            )
    except Exception as e:
        logger.error(e)
        raise e
