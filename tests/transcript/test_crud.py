from unittest import mock

# Need to mock this before imports, as the client authorizes on creation
mock.patch('google.cloud.speech_v1p1beta1.SpeechClient').start()
mock.patch('google.cloud.storage.Client').start()
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.audio import models as am
from app.transcript import crud as tc
from app.transcript import models as tm
import pytest


class TestTranscript:

    def setup_method(self, method):
        self.google_transcriber_mock = mock.patch("app.transcript.crud.transcriber").start()

    def teardown_method(self, method):
        self.google_transcriber_mock.stop()

    def test_create_transcript(self, db_session: Session):
        EXTERNAL_ID = "12345"
        a = am.Audio(location='/tmp/test', size=123, original_filename='123.mp3')
        cfg = tm.TranscriptConfig(language='english', provider='google', config='{"foo":123}')
        db_session.add_all([a, cfg])
        db_session.commit()
        self.google_transcriber_mock.create = mock.Mock(return_value=EXTERNAL_ID)
        t = tc.create_transcript(db_session, a.id, tm.TranscriptLanguageEnum.ENGLISH)
        t_from_db = db_session.query(tm.Transcript).filter(tm.Transcript.id == t.id).first()
        assert t_from_db
        assert t_from_db.external_id == EXTERNAL_ID
        assert t_from_db.audio_id == a.id

    def test_create_transcript_db_errors(self, db_session: Session):
        # We can't create transcript without audio
        with pytest.raises(tc.NotFound):
            t = tc.create_transcript(db_session, 1, tm.TranscriptLanguageEnum.ENGLISH)

        # Nothing works if config for recognizer is not specified
        with pytest.raises(tc.NotFound):
            a = am.Audio(location='/tmp/test', size=123, original_filename='123.mp3')
            db_session.add(a)
            db_session.commit()
            tc.create_transcript(db_session, a.id, tm.TranscriptLanguageEnum.ENGLISH)

        # We can't create two transcripts origination from the same audiofile
        cfg = tm.TranscriptConfig(language='english', provider='google', config='{"foo":123}')
        db_session.add(cfg)
        db_session.commit()
        self.google_transcriber_mock.create = mock.Mock(return_value="12345")
        tc.create_transcript(db_session, a.id, tm.TranscriptLanguageEnum.ENGLISH)
        with pytest.raises(tc.AlreadyExists):
            tc.create_transcript(db_session, a.id, tm.TranscriptLanguageEnum.ENGLISH)

        # We try to delete the transcription request if something goes wrong with the database
        a2 = am.Audio(location='/tmp/test', size=123, original_filename='1234.mp3')
        db_session.add(a2)
        db_session.commit()
        self.google_transcriber_mock.delete = mock.MagicMock()
        db_session.commit = mock.MagicMock(side_effect=IntegrityError('123', '123', '123'))
        with pytest.raises(IntegrityError):
            t = tc.create_transcript(db_session, a2.id, tm.TranscriptLanguageEnum.ENGLISH)
        self.google_transcriber_mock.delete.assert_called_once()

    def test_create_transcript_transcriber_errors(self, db_session: Session):
        a = am.Audio(location='/tmp/test', size=123, original_filename='123.mp3')
        cfg = tm.TranscriptConfig(language='english', provider='google', config='{"foo":123}')
        db_session.add_all([a, cfg])
        db_session.commit()
        # self.google_transcriber_mock.create = mock.Mock(side_effect=Exception('Some Exception'))
        # t = tc.create_transcript(db_session, a.id, tm.TranscriptLanguageEnum.ENGLISH)

