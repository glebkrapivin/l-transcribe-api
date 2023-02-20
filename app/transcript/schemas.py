import json
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any

from pydantic import BaseModel, validator


class TranscriptStatusEnum(str, Enum):
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILURE = "failure"


class TranscriptLanguageEnum(str, Enum):
    ENGLISH = 'english'
    SPANISH = 'spanish'


class TranscriptBase(BaseModel):
    audio_id: int
    language: TranscriptLanguageEnum

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


class TranscriptConfigBase(BaseModel):
    language: TranscriptLanguageEnum
    config: Dict[str, Any]
    provider: str

    @validator('config', pre=True)
    def make_config_json(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v
    class Config:
        orm_mode = True


class TranscriptConfigCreate(TranscriptConfigBase):
    pass


class TranscriptConfigUpdate(TranscriptConfigBase):
    pass


class TranscriptConfig(TranscriptConfigBase):
    id: int
