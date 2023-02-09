from datetime import datetime

from pydantic import BaseModel


class Audio(BaseModel):
    id: int
    location: str
    created_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True
