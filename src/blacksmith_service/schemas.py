from pydantic import BaseModel
from typing import Optional


class MessageRequest(BaseModel):
    message: Optional[str] = None


class MessageResponse(BaseModel):
    message: str
    status: str
    processed: bool
