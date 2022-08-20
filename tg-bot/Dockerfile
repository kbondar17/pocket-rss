# syntax=docker/dockerfile:1
FROM python:3.9-slim

ENV PYTHONUNBUFFERED=True \
    POETRY_VIRTUALENVS_CREATE=False

WORKDIR /app
EXPOSE 2000

RUN pip install poetry

COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-dev
# RUN pip install feedparser
# RUN pip install validators
# RUN pip install bs4

COPY weedly_bot /app/weedly_bot


CMD [ "python", "-m", "weedly_bot"]
