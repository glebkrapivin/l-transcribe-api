from abc import abstractmethod, ABCMeta
from typing import List, Dict, Any, Optional
from typing import Union

from pydantic import BaseModel


class WordDto(BaseModel):
    word: str
    start_at: int
    end_at: int
    speaker_tag: Optional[int]


class TranscriptDto(BaseModel):
    external_id: int
    is_ready: bool
    words: Optional[List[WordDto]]
    metadata: Optional[Dict[str, Any]]


class BaseTranscriber(metaclass=ABCMeta):

    @abstractmethod
    def create(self, config: str, audio_location: str) -> str:
        pass

    @abstractmethod
    def delete(self, ext_transcript_id: Union[str, int]) -> None:
        pass

    @abstractmethod
    def get(self, ext_transcript_id: Union[str, int]) -> TranscriptDto:
        pass

    @abstractmethod
    def is_ready(self, ext_transcript_id: Union[str, int]) -> bool:
        pass
