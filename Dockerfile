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

RUN pip install --no-cache-dir "gunicorn==21.0.1"

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

WORKDIR /app

RUN chown wagtail:wagtail /app

COPY --chown=wagtail:wagtail . .

USER wagtail

ENV DJANGO_SETTINGS_MODULE=stl.settings.production
RUN python manage.py collectstatic --noinput --clear

CMD ["gunicorn", "stl.wsgi:application"]
