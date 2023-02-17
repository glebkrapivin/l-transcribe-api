from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel


class TranscriptStatusEnum(str, Enum):
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILURE = "failure"


class TranscriptBase(BaseModel):
    audio_id: int

    class Config:
        orm_mode = True


class TranscriptCreate(TranscriptBase):
    pass


class Transcript(TranscriptBase):
    id: int
    status: TranscriptStatusEnum
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()


class TranscriptDetail(Transcript):
    text: str


class TranscriptItemBase(BaseModel):
    start_at: int
    stop_at: int
    text: str

    class Config:
        orm_mode = True


class AnalysisItem(BaseModel):
    transcript_id: int
    filename: str
    audio_id: int
    start_at: int

    class Config:
        orm_mode = True


class Analysis(BaseModel):
    word: str
    items: List[AnalysisItem]

    class Config:
        orm_mode = True
