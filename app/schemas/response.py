from pydantic import BaseModel
from typing import Optional


class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    success: bool
    error: str
    message: str
