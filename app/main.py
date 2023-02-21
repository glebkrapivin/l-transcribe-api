import logging

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from starlette.middleware import Middleware

from app.audio.api import v1 as av1
from app.core.config import settings
from app.transcript.api import v1 as tv1

logging.basicConfig(level='DEBUG',
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s')


def get_application():
    cors = Middleware(
        CORSMiddleware,
        # allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_origins=["*"],
        # allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app = FastAPI(title=settings.PROJECT_NAME, middleware=[cors], dependencies=[Depends(basic_verify_password)])
    return _app


security = HTTPBasic()


def basic_verify_password(sec: HTTPBasicCredentials = Depends(security)):
    # TODO: it is not really security, as the password is stored plain text
    #   just a super-fast way to expose endpoints online for product demo
    logging.info('Was here')
    if sec.username == 'admin' and sec.password == 'whereismydemo':
        return True
    raise HTTPException(status_code=401, detail='Permission denied', headers={"WWW-Authenticate": "Basic"},
                        )


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

# import logging
# from fastapi import FastAPI, Request, status
# from fastapi.exceptions import RequestValidationError
# from fastapi.responses import JSONResponse
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
# 	exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
# 	logging.error(f"{request}: {exc_str}")
# 	content = {'status_code': 10422, 'message': exc_str, 'data': None}
# 	return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
