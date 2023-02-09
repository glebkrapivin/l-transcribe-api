from typing import List, Optional

from fastapi import APIRouter

from app.transcript.schemas import TranscriptStatusEnum, TranscriptRequest, TranscriptResponse, \
    TranscriptWordsResponse

router = APIRouter(prefix="/v1")


@router.post("/transcript", tags=["Transcript"])
def create_new_transcript(transcript_request: TranscriptRequest) -> TranscriptResponse:
    # TODO:
    #  1. Sync upload / save
    return TranscriptResponse(id=5, status=TranscriptStatusEnum.IN_PROGRESS)


@router.get("/transcript/{transcript_id}", tags=["Transcript"])
def get_transcript_by_id(transcript_id: int) -> TranscriptResponse:
    return TranscriptResponse(id=5, status=TranscriptStatusEnum.IN_PROGRESS)


@router.get("/transcript/{transcript_id}/words", tags=["Transcript"])
def get_transcript_words_by_id(transcript_id: int) -> TranscriptWordsResponse:
    return TranscriptWordsResponse()


@router.get("/transcript", tags=["Transcript"])
def list_transcripts() -> Optional[List[TranscriptResponse]]:
    return []
