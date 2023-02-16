from datetime import datetime

from pydantic import BaseModel


class AudioBase(BaseModel):
    class Config:
        orm_mode = True


class AudioCreate(AudioBase):
    # audio is created with file
    pass


class Audio(AudioBase):
    id: int
    location: str
    created_at: datetime = datetime.utcnow()
