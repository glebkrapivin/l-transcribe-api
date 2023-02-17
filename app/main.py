from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

from app.core.config import settings
from app.transcript.api import v1 as tv1
from app.audio.api import v1 as av1


def get_application():
    cors = Middleware(
        CORSMiddleware,
        # allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_origins=["*"],
        # allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app = FastAPI(title=settings.PROJECT_NAME, middleware=[cors])
    return _app


app = get_application()
app.include_router(tv1.router)
app.include_router(av1.router)
app.mount(
    "/",
    StaticFiles(
        directory="app/transcript/static",
        html=True,
    ),
)


