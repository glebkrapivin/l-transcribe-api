import dataclasses
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

import app.transcript.schemas as s
import app.transcript.models as m
import app.transcript.crud as c
from app.audio.api.v1 import get_db



router = APIRouter(prefix="/api/v1")


@router.post("/transcript", tags=["Transcript"], response_model=s.Transcript)
def create_new_transcript(
    transcript_request: s.TranscriptCreate, db: Session = Depends(get_db)
):
    try:
        t = c.create_transcript(db, transcript_request.audio_id)
    except c.NotFound:
        raise HTTPException(status_code=400, detail="No audio_id found")
    except c.AlreadyExists:
        raise HTTPException(
            status_code=400, detail="Transcript with this audio already exists"
        )
    return t


@router.get(
    "/transcript/{transcript_id}", tags=["Transcript"], response_model=s.TranscriptDetail
)
def get_transcript_by_id(transcript_id: int, db: Session = Depends(get_db)):
    return db.query(m.Transcript).filter(m.Transcript.id == transcript_id).first()


@router.get(
    "/transcript/{transcript_id}/words",
    tags=["Transcript"],
    response_model=List[s.TranscriptItemBase],
)
def get_transcript_words_by_id(transcript_id: int, db: Session = Depends(get_db)):
    # TODO: Don't know how to get the actual text of the word here
    #   so did conversion manually

    transcript_words = c.get_transcript_words(db, transcript_id)
    result = []
    for transcript_item in transcript_words:
        obj = s.TranscriptItemBase(
            start_at=transcript_item.start_at,
            stop_at=transcript_item.stop_at,
            text=transcript_item.word.text,
        )
        result.append(obj)
    return result


@router.get("/transcript", tags=["Transcript"], response_model=List[s.Transcript])
def list_transcripts(external_id: Optional[int] = None, db: Session = Depends(get_db)):
    return c.list_transcripts(db, external_id)


@router.get("/analysis", tags=["Analysis"], response_model=s.Analysis)
def get_transcripts_by_word(word: str, db: Session = Depends(get_db)):
    tw = c.get_transcripts_by_word(db, word)
    an_items = []
    for transcript_item in tw:
        obj = s.AnalysisItem(
            transcript_id=transcript_item.transcript_id,
            start_at=transcript_item.start_at,
            filename=transcript_item.transcript.audio.original_filename,
            audio_id=transcript_item.transcript.audio_id,
        )
        an_items.append(obj)
    result = s.Analysis(word=word, items=an_items)
    return result
