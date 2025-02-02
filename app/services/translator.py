from googletrans import Translator
from app.database.session import AsyncSessionLocal
from app.schemas.faq import FAQ as FAQSchema
from loguru import logger
from app.models.faq import FAQTranslation as FAQTranslationModels
from app.core import constants
import asyncio

translator = Translator()


async def translate_text(faq: FAQSchema):
    try:
        translations = []

        async def translate_and_store(lang):
            translated_question = await translator.translate(
                text=faq.question,
                dest=lang,
            )
            translated_answer = await translator.translate(
                text=faq.answer,
                dest=lang,
            )
            translations.append(
                FAQTranslationModels(
                    faq_id=faq.id,
                    translated_question=translated_question.text,
                    translated_answer=translated_answer.text,
                    language=lang,
                )
            )

        await asyncio.gather(
            *(
                translate_and_store(lang)
                for lang in constants.SUPPORTED_LANGUAGES  # noqa
            )
        )
        async with AsyncSessionLocal() as db:
            db.add_all(translations)
            await db.commit()
    except Exception as e:
        logger.error(e)
        raise e
