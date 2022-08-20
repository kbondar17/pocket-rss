# syntax=docker/dockerfile:1
FROM python:3.9-slim

ENV PYTHONUNBUFFERED=True \
    POETRY_VIRTUALENVS_CREATE=False

WORKDIR /app
EXPOSE 5000

RUN pip install poetry

COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-dev

COPY rssparser /app/rssparser

CMD [ "poetry", "run", "python", "-m", "rssparser"]
