import os
import shutil
from io import BytesIO

from fastapi import UploadFile
from pydub import AudioSegment

from app.core.config import settings
from app.transcript.schemas import Audio


def get_raw_bytes(audio_id, start, end) -> BytesIO:
    audio = Audio(location='/Users/gkrapivin/repos/gkrapivin/leela/data/zagit/20230204/3_min_rec.mp3', id=1)
    audiosegment = AudioSegment.from_mp3(audio.location)
    b = BytesIO()
    if start and end:
        audiosegment = audiosegment[start: end]
    audiosegment.export(b)
    return b


def create(b: UploadFile):
    filepath = os.path.join(settings.AUDIOFILES_DIRECTORY, b.filename)
    f = open(filepath, 'wb')
    shutil.copyfileobj(b.file, f)
    # TODO:
    #   - add to the database


def delete_by_id(audio_id):
    # TODO:
    #    delete the file
    #    delete from the database
    pass
