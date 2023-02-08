from typing import Union, List, Optional

from fastapi import APIRouter

from app.transcript.schemas import Audio, TranscriptStatusEnum, TranscriptRequest, TranscriptResponse, TranscriptWordsResponse

router = APIRouter()

sample_audio = Audio(id=1, filename='test.gzip', status=TranscriptStatusEnum.IN_PROGRESS)


@router.post("/audio/", tags=["Audio"])
def upload_an_audio_for_transcript():  # file: bytes = File()):
    # TODO:
    #  1. Sync upload / save
    return sample_audio


@router.get('/audio/{audio_id}', tags=["Audio"])
def get_audio_by_id(audio_id: int):
    return sample_audio

@router.get('/audio/{audio_id}/raw', tags=["Audio"])
def get_raw_audio_by_id(audio_id: int):
    return bytes()

@router.delete('/audio/{audio_id}', status_code=204, tags=["Audio"])
def delete_audio_by_id(audio_id:int):
    pass

@router.post("/transcript", tags=["Transcript"])
def create_new_transcript(transcript_request: TranscriptRequest) -> TranscriptResponse:  # file: bytes = File()):
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