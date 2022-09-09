# syntax=docker/dockerfile:1
FROM python:3.9-slim

ENV PYTHONUNBUFFERED=True \
    POETRY_VIRTUALENVS_CREATE=False

WORKDIR /app
EXPOSE 5000

# RUN pip install poetry

# COPY pyproject.toml poetry.lock /app/
# RUN poetry install --no-dev
RUN apt-get update && apt-get -y install cron
RUN apt-get -y install vim

# Cronjob (процесс, который следит, чтобы не было больше 30 статей на фид)
COPY ./newest_articles_cron.sh /etc/cron.d/newest_articles_cron.sh
RUN chmod 0644 /etc/cron.d/newest_articles_cron.sh
RUN crontab /etc/cron.d/newest_articles_cron.sh
RUN touch /var/log/cron.log
RUN service cron start

COPY weedly /app/weedly
COPY requirements.txt /app/ 
COPY ./docker_commands/init_db.sh /app/init_db.sh
COPY prod.env /app/

RUN pip install -r requirements.txt

# CMD [ "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "weedly.app:app"]
