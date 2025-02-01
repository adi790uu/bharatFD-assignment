from fastapi import HTTPException
from sqlalchemy import Column, Integer, String, Text, ForeignKey, select, delete  # noqa
from sqlalchemy.orm import relationship, selectinload
from app.database.base import Base
from sqlalchemy.ext.asyncio import AsyncSession


class FAQ(Base):
    __tablename__ = "faqs"

    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    language = Column(String(10), nullable=False)
    translations = relationship(
        "FAQTranslation", back_populates="faq", cascade="all, delete-orphan"
    )

    @classmethod
    async def delete_faq(cls, faq_id: int, db: AsyncSession):
        faq_instance = await db.execute(select(cls).where(cls.id == faq_id))
        if not faq_instance.scalars().first():
            raise HTTPException(status_code=404, detail="FAQ not found")

        await db.execute(delete(cls).where(cls.id == faq_id))
        await db.commit()

    @classmethod
    async def create_faq(
        cls, question: str, answer: str, language: str, db: AsyncSession
    ):
        faq_instance = cls(question=question, answer=answer, language=language)
        db.add(faq_instance)
        await db.commit()
        await db.refresh(faq_instance)
        return faq_instance

    @classmethod
    async def get_translated_text(cls, lang: str, db: AsyncSession) -> dict:

        faq_instance = await db.execute(
            select(cls).options(selectinload(cls.translations))
        )

        faqs_instances = faq_instance.scalars().all()
        if not faq_instance:
            raise HTTPException(status_code=400)

        translated_faqs = []

        for faq_instance in faqs_instances:
            for translation in faq_instance.translations:
                if translation.language == lang:
                    translated_faqs.append(
                        {
                            "id": translation.faq_id,
                            "question": translation.translated_question,
                            "answer": translation.translated_answer,
                        }
                    )
        return translated_faqs


class FAQTranslation(Base):
    __tablename__ = "faq_translations"

    faq_id = Column(Integer, ForeignKey("faqs.id", ondelete="CASCADE"))
    language = Column(String(10), nullable=False)
    translated_question = Column(Text, nullable=False)
    translated_answer = Column(Text, nullable=False)

    faq = relationship("FAQ", back_populates="translations")

    @classmethod
    async def add_faq_translation(
        cls,
        db: AsyncSession,
        translated_question: str,
        faq_id: int,
        translated_answer: str,
        lang: str,
    ):
        translation_instance = cls(
            faq_id=faq_id,
            translated_question=translated_question,
            translated_answer=translated_answer,
            language=lang,
        )
        db.add(translation_instance)
        await db.commit()
        await db.refresh(translation_instance)
        return translation_instance
