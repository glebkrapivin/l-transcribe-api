import datetime
import json
import logging
from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import func

import app.audio.crud as a_crud
import app.transcript.models as m
from app.transcript.transcribers import google_s2t


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
        raise AlreadyExists()
    external_id = google_s2t.create_transcript_request(conf.config, audio.location)
    t = m.Transcript(audio_id=audio_id, status=m.TranscriptStatusEnum.IN_PROGRESS, external_id=external_id,
                     language=language)
    db.add(t)
    try:
        db.commit()
    except IntegrityError:
        google_s2t.try_delete_transcript_request(t.external_id)
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
            finished = google_s2t.get_transcript_status(t.external_id)
            if finished:
                result, uri = google_s2t.get_transcript_result(t.external_id)
                words = result.results[-1].alternatives[0].words
                for word in words:
                    start_at = word.start_time.total_seconds() * 1000
                    stop_at = word.end_time.total_seconds() * 1000
                    text = word.word
                    speaker_tag = word.speaker_tag
                    t_item = m.TranscriptItem(transcript_id=t.id, speaker_tag=speaker_tag,
                                              start_at=start_at, stop_at=stop_at, word=text)
                    t_items.append(t_item)
                t.status = m.TranscriptStatusEnum.SUCCESS
                t.updated_at = datetime.datetime.utcnow()
                logging.info('Marking successful trasnscript_id=%s', t.id)
                google_s2t.delete_audio(uri, "leela_bucket")
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
