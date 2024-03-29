FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

ENV PYTHONPATH "${PYTHONPATH}:/"
ENV PORT=8000

RUN apt update && apt install -y ffmpeg

RUN pip install --upgrade pip

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app
