from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from app.database import Base

class Audio(Base):

    id = Column(Integer, primary_key=True)  # type: ignore
    location = Column(String)  # type: ignore
    size = Column(Float, nullable=True)  # type: ignore
    created_at = Column(DateTime, server_default=func.now())  # type: ignore
