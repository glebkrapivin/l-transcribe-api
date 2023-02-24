import datetime
import json
import logging
from typing import List

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import app.audio.crud as a_crud
import app.transcript.models as m
from app.transcript.transcribers.google import GoogleTranscriber

transcriber = GoogleTranscriber()


class NotFound(Exception):
    pass


class AlreadyExists(Exception):
    pass


def create_transcript(db: Session, audio_id: int, language: m.TranscriptLanguageEnum):
    audio = a_crud.get_by_id(db, audio_id)
    if not audio:
        raise NotFound()

    conf = db.query(m.TranscriptConfig) \
        .filter(m.TranscriptConfig.language == language) \
        .filter(m.TranscriptConfig.provider == 'google') \
        .first()
    if not conf:
        raise NotFound('Config not found')

    aud = db.query(m.Transcript) \
        .filter(m.Transcript.audio_id == audio_id).first()
    if aud:
        raise AlreadyExists('Transcript from this audio already exists')
    external_id = transcriber.create(conf.config, audio.location)
    t = m.Transcript(audio_id=audio_id, status=m.TranscriptStatusEnum.IN_PROGRESS, external_id=external_id,
                     language=language)
    db.add(t)
    try:
        db.commit()
    except IntegrityError:
        transcriber.delete(t.external_id)
        raise
    return t


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


def get_transcript_by_id(db: Session, transcript_id: int) -> m.Transcript:
    t = db.query(m.Transcript).filter(m.Transcript.id == transcript_id).first()
    if not t:
        return None
    if len(t.items) > 0:  # type:ignore
        t.text = ' '.join([_.word for _ in t.items])  # type: ignore
    return t


def get_transcript_words(db: Session, transcript_id: int) -> List[m.TranscriptItem]:
    items = (
        db.query(m.TranscriptItem)
        .filter(m.TranscriptItem.transcript_id == transcript_id)
        .all()
    )
    return items


def get_transcripts_by_word(db: Session, word: str):
    items = db.query(m.TranscriptItem).filter(func.lower(m.TranscriptItem.word) == word.lower()).all()
    return items


def update_transcripts_status(db: Session):
    # - Fetch statuses from Google speech-to-text provider
    # - Update words from them
    logging.info('Started querying google')
    not_finished = db.query(m.Transcript).filter(
        m.Transcript.status == m.TranscriptStatusEnum.IN_PROGRESS).with_for_update().all()
    logging.info('Got %s unfinished transcripts', len(not_finished))
    t_items = []
    for t in not_finished:
        if t.external_id:
            logging.info("Doing transcript with external_id=%s", t.external_id)
            finished = transcriber.is_ready(t.external_id)
            if finished:
                tdto = transcriber.get(t.external_id)
                for word in tdto.words:
                    t_items.append(m.TranscriptItem(transcript_id=t.id, start_at=word.start_at, stop_at=word.end_at,
                                                    speaker_tag=word.speaker_tag, word=word.word))
                t.status = m.TranscriptStatusEnum.SUCCESS
                t.updated_at = datetime.datetime.utcnow()
                logging.info('Marking successful trasnscript_id=%s', t.id)
    db.add_all(t_items)
    db.commit()


def get_transcript_config(config_id: int, db: Session):
    return db.query(m.TranscriptConfig).filter(m.TranscriptConfig.id == config_id).first()


def create_transcript_config(language: m.TranscriptLanguageEnum, provider: str, config: str, db: Session):
    c = m.TranscriptConfig(language=language, provider=provider, config=json.dumps(config))
    db.add(c)
    db.commit()
    return c


def update_transcript_config(config_id: int, language: m.TranscriptLanguageEnum, provider: str, config: str,
                             db: Session):
    c = get_transcript_config(config_id, db)
    if not c:
        return None
    c.config = json.dumps(config)
    c.language = language
    c.provider = provider
    db.commit()
    return c
