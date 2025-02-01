from pydantic import BaseModel


class CreateFAQRequest(BaseModel):
    question: str
    answer: str
