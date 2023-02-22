import pytest
from app.transcript import models as tm
from app.transcript import crud as tc
from app.audio import models as am
from app.audio import crud as ac
from sqlalchemy.orm import Session
from unittest.mock import patch


def test_true(db_session: Session,c, c2):
    a = am.Audio(location='/tmp/test', size=123)
    db_session.add(a)
    db_session.commit()

    assert db_session.query(am.Audio).all()