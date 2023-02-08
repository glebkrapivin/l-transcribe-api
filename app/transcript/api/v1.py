from fastapi import APIRouter

router = APIRouter()


@router.get("/users/me")
def get_transcript():
    return "transcript app created!"
