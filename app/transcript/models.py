from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
    ForeignKey,
    Enum,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base
from app.transcript.schemas import TranscriptStatusEnum, TranscriptLanguageEnum

#
# class Word(Base):
#     id = Column(Integer, primary_key=True)
#     text = Column(String)
#
#     __table_args__ = (UniqueConstraint("text", name="one_text"),)


class Transcript(Base):
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=True)
    status = Column(
        Enum(TranscriptStatusEnum),
        nullable=False,
        default=TranscriptStatusEnum.IN_PROGRESS,
    )
    language = Column(Enum(TranscriptLanguageEnum), nullable=False, default=TranscriptLanguageEnum.ENGLISH,
                      server_default=TranscriptLanguageEnum.ENGLISH.upper())
    audio_id = Column(Integer, ForeignKey("audio.id"))
    external_id = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())  # type: ignore
    updated_at = Column(DateTime, server_default=func.now())  # type: ignore

    items = relationship("TranscriptItem", back_populates="transcript")
    audio = relationship("Audio")
    __table_args__ = (UniqueConstraint("external_id", name="one_external_id"),
                      UniqueConstraint("audio_id", name="one_audio_id")
                      )


class TranscriptItem(Base):
    id = Column(Integer, primary_key=True)
    transcript_id = Column(Integer, ForeignKey("transcript.id"))
    # word_id = Column(Integer, ForeignKey("word.id"))
    start_at = Column(Integer)
    stop_at = Column(Integer)
    speaker_tag = Column(Integer, nullable=True)

    word = Column(Text, nullable=False)
    # word = relationship("Word")
    transcript = relationship("Transcript", back_populates="items")
