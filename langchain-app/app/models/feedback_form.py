from typing import Optional

from pydantic import BaseModel


class FeedbackForm(BaseModel):
    user: str
    id: str
    service_type: str
    feedback: Optional[str] = None
    written_feedback: Optional[str] = None
