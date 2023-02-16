from app.audio.models import Audio
from app.transcript.models import Transcript, TranscriptItem, Word
from app.database import SessionLocal

import random
import string


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str


def get_or_create(model, **kwargs):
    db = SessionLocal()
    instance = db.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        db.add(instance)
        db.commit()
        return instance


def init_db():
    db = SessionLocal()


    words = [Word(text=get_random_string(10)) for i in range(10000)]
    db.add_all(words)
    db.commit()



    for i in range(150):
        a = Audio(
            location=get_random_string(5),
            original_filename=get_random_string(10) + ".mp3",
        )
        t = Transcript(
            audio=a,
            text=" ".join([get_random_string(10) for _ in range(10)]),
            external_id=random.randint(1, 10000),
        )
        titemsraw = [
            [random.randint(1, 9999), _, _ + 1] for _ in range(random.randint(1, 500))
        ]
        titems = []
        for text, start_at, end_at in titemsraw:
            titems.append( TranscriptItem(
                transcript=t,
                start_at=start_at,
                stop_at=end_at,
                word_id=text
            ))
        db.add_all([a, t])
        db.add_all(titems)
        # try:
        #     db.commit()
        # except:
        #     pass
        db.commit()


if __name__ == "__main__":
    init_db()
