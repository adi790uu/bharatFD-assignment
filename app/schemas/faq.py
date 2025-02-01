from pydantic import BaseModel


class FAQ(BaseModel):
    id: int
    question: str
    answer: str
