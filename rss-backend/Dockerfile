# syntax=docker/dockerfile:1
FROM python:3.9-slim

ENV PYTHONUNBUFFERED=True \
    POETRY_VIRTUALENVS_CREATE=False

WORKDIR /app
EXPOSE 5000

# RUN pip install poetry

# COPY pyproject.toml poetry.lock /app/
# RUN poetry install --no-dev

COPY weedly /app/weedly
COPY requirements.txt /app/ 
COPY godb.sh /app/
RUN pip install -r requirements.txt
# RUN python -m weedly.db create
# RUN python -m weedly.db add-test-rss

CMD [ "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "weedly.app:app"]
