from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import app.audio.crud as a_crud
import app.transcript.models as m


class NotFound(Exception):
    pass


class AlreadyExists(Exception):
    pass


def create_transcript(db: Session, audio_id: int, language: m.TranscriptLanguageEnum):
    audio = a_crud.get_by_id(db, audio_id)
    if not audio:
        raise NotFound()

    import random
    external_id = random.randint(1, 50000)
    t = m.Transcript(audio_id=audio_id, status=m.TranscriptStatusEnum.IN_PROGRESS, external_id=external_id,
                     language=language)
    db.add(t)
    try:
        db.commit()
    except IntegrityError:
        raise AlreadyExists()
    return t


def send_transcriber_task():
    pass


def list_transcripts(db: Session, external_id: int = None) -> List[m.Transcript]:
    if external_id:
        t = (
            db.query(m.Transcript)
            .filter(m.Transcript.external_id == external_id)
            .first()
        )
        if not t:
            return []
        return [t]
    return db.query(m.Transcript).all()


def get_transcript_words(db: Session, transcript_id: int) -> List[m.TranscriptItem]:
    items = (
        db.query(m.TranscriptItem)
        .filter(m.TranscriptItem.transcript_id == transcript_id)
        .all()
    )
    return items


def get_transcripts_by_word(db: Session, word: str):
    items = db.query(m.TranscriptItem).filter(m.TranscriptItem.word.has(text=word)).all()
    return items
