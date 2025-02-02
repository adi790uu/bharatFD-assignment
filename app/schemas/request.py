from typing import Optional
from pydantic import BaseModel


class CreateFAQRequest(BaseModel):
    question: str
    language: Optional[str] = None
    answer: str
