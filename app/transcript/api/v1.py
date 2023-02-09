from typing import List, Optional, Union

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from fastapi import UploadFile

from app.transcript import audio as a
from app.transcript.schemas import Audio, TranscriptStatusEnum, TranscriptRequest, TranscriptResponse, \
    TranscriptWordsResponse

router = APIRouter()

sample_audio = Audio(id=1, location='test.gzip', status=TranscriptStatusEnum.IN_PROGRESS)


@router.post("/audio/", tags=["Audio"])
def upload_an_audio_for_transcript(file: UploadFile):
    # TODO:
    #  1. Sync upload / save
    if "mp3" not in file.filename:
        raise HTTPException(status_code=400, detail="Only MP3 files are accepted.")

    audio = a.create(file)
    return audio


@router.get('/audio/{audio_id}', tags=["Audio"])
def get_audio_by_id(audio_id: int):
    return sample_audio


@router.get('/audio/{audio_id}/raw', tags=["Audio"], response_class=StreamingResponse)
def get_raw_audio_by_id(audio_id: int, start: Union[int, None] = None,
                        end: Union[int, None] = None) -> StreamingResponse:
    if bool(start) != bool(end):
        raise HTTPException(status_code=400, detail='Specify both "start" and "end"')
    if end <= start:
        raise HTTPException(status_code=400, detail='"end" cannot be less than "start"')
    audio = a.get_raw_bytes(audio_id, start, end)
    return StreamingResponse(audio, media_type="audio/mp3")


@router.delete('/audio/{audio_id}', status_code=204, tags=["Audio"])
def delete_audio_by_id(audio_id: int):
    pass


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
