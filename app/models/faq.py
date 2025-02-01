from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base
from sqlalchemy.ext.asyncio import AsyncSession


class FAQ(Base):
    __tablename__ = "faqs"

    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)

    translations = relationship(
        "FAQTranslation", back_populates="faq", cascade="all, delete-orphan"
    )

    @classmethod
    async def create_faq(cls, question: str, answer: str, db: AsyncSession):
        faq_instance = cls(question=question, answer=answer)
        db.add(faq_instance)
        await db.commit()
        await db.refresh(faq_instance)
        return faq_instance

    def get_translated_text(self, lang: str) -> dict:
        for translation in self.translations:
            if translation.language == lang:
                return {
                    "question": translation.translated_question,
                    "answer": translation.translated_answer,
                }
        return {
            "question": self.question,
            "answer": self.answer,
        }


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
