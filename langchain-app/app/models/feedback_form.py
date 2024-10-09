from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class FeedbackForm(BaseModel):
    user: str
    feedback: Optional[str] = None
    written_feedback: Optional[str] = None
    created_at: datetime | str = None
