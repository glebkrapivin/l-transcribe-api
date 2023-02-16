from typing import List, Union

from fastapi import APIRouter, HTTPException, Depends
from fastapi import UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.audio import crud as a, schemas as s
from app.audio.crud import FilenameExists
from app.core.utils import get_db

router = APIRouter(prefix="/api/v1", tags=["Audio"])


@router.post("/audio/", )
def upload_an_audio_for_transcript(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # TODO:
    #  1. Sync upload / save
    if "mp3" not in file.filename or file.content_type != "audio/mpeg":
        raise HTTPException(status_code=400, detail="Only MP3 files are accepted.")
    try:
        audio = a.create(db, file)
    except FilenameExists:
        raise HTTPException(status_code=400, detail='File with this name already exists')
    return audio


@router.get('/audio/{audio_id}', )
def get_audio_by_id(audio_id: int, db: Session = Depends(get_db)) -> s.Audio:
    audio = a.get_by_id(db, audio_id)
    if not audio:
        raise HTTPException(status_code=404)
    return audio


@router.get('/audio', )
def list_audio(db: Session = Depends(get_db)) -> List[s.Audio]:
    return a.list_audio(db)


@router.get('/audio/{audio_id}/raw', response_class=StreamingResponse)
def get_raw_audio_by_id(audio_id: int, start: Union[int, None] = None,
                        end: Union[int, None] = None, db: Session = Depends(get_db)) -> StreamingResponse:
    if bool(start) != bool(end):
        raise HTTPException(status_code=400, detail='Specify both "start" and "end"')
    if end <= start:
        raise HTTPException(status_code=400, detail='"end" cannot be less than "start"')
    audio = a.get_raw_bytes(db, audio_id, start, end)
    return StreamingResponse(audio, media_type="audio/mp3")


@router.delete('/audio/{audio_id}', status_code=204, )
def delete_audio_by_id(audio_id: int, db: Session = Depends(get_db)):
    if not a.delete_by_id(db, audio_id):
        raise HTTPException(status_code=404)
