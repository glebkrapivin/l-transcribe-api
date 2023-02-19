from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

ca = {}
if "sqlite" in settings.DB_URI:
    ca = {"check_same_thread": False}

engine = create_engine(settings.DB_URI, pool_pre_ping=True, connect_args=ca)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@as_declarative()
class Base:

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
