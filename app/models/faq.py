from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base


class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)

    translations = relationship(
        "FAQTranslation", back_populates="faq", cascade="all, delete-orphan"
    )

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

    id = Column(Integer, primary_key=True, index=True)
    faq_id = Column(Integer, ForeignKey("faqs.id", ondelete="CASCADE"))
    language = Column(String(10), nullable=False)
    translated_question = Column(Text, nullable=False)
    translated_answer = Column(Text, nullable=False)

    faq = relationship("FAQ", back_populates="translations")
