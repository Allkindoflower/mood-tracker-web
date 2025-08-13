from pydantic import BaseModel
from typing import Optional

class MoodEntry(BaseModel):
    mood: str
    sentiment: Optional[str] = None
