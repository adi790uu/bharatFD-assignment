from pydantic import BaseModel


class CreateFAQRequest(BaseModel):
    question: str
    language: str
    answer: str
