from pydantic import BaseModel

class MoodEntry(BaseModel):
    mood: str