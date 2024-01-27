FROM python:3.12-slim
RUN useradd wagtail

EXPOSE 8000

ENV PYTHONUNBUFFERED=1 \
    PORT=8000

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

RUN pip install uvicorn gunicorn

COPY requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /app

RUN chown wagtail:wagtail /app

COPY --chown=wagtail:wagtail . .
USER wagtail
CMD gunicorn stl.asgi:application -k uvicorn.workers.UvicornWorker
