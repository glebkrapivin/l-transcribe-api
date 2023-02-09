from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel


class TranscriptStatusEnum(str, Enum):
    IN_PROGRESS = 'in_progress'
    SUCCESS = 'success'
    FAILURE = 'failure'


class TranscriptRequest(BaseModel):
    audio_id: int


class TranscriptItem(BaseModel):
    start: int
    end: int
    text: str


class TranscriptResponse(BaseModel):
    id: int
    status: TranscriptStatusEnum
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
    items: List[TranscriptItem] = None


class TranscriptWordsResponse(BaseModel):
    items: List[TranscriptItem] = None


class Audio(BaseModel):
    id: int
    location: str
    created_at: datetime = datetime.utcnow()

    class Config:
        orm_mode = True
