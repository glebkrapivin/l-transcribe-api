import os
import shutil
import uuid
from io import BytesIO

from fastapi import UploadFile
from pydub import AudioSegment
from sqlalchemy.orm import Session

from app.audio import models as m
from app.core.config import settings


def get_raw_bytes(db: Session, audio_id: int, start: int, end: int) -> BytesIO:
    audio = get_by_id(db, audio_id)
    audiosegment = AudioSegment.from_mp3(audio.location)
    b = BytesIO()
    if start and end:
        audiosegment = audiosegment[start: end]
    audiosegment.export(b)
    return b


def create(db: Session, b: UploadFile):
    _uuid = str(uuid.uuid4())
    filepath = os.path.join(settings.AUDIOFILES_DIRECTORY, _uuid)
    f = open(filepath, 'wb')
    shutil.copyfileobj(b.file, f)
    db_audio = m.Audio(location=filepath)
    db.add(db_audio)
    db.commit()
    return db_audio


def delete_by_id(db: Session, audio_id: int):
    if not get_by_id(db, audio_id):
        return None
    db.query(m.Audio).filter(m.Audio.id == audio_id).delete()
    db.commit()


def get_by_id(db: Session, audio_id: int):
    return db.query(m.Audio).filter(m.Audio.id == audio_id).first()


def list_audio(db: Session):
    res = db.query(m.Audio).all()
    print(res)
    return res
