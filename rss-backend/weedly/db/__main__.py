import logging
from pathlib import Path
from statistics import mode

import orjson
from typer import Typer

from weedly.db.models import Feed, Article
from weedly.db.session import create_db, db_session, reset_db

app = Typer()
logger = logging.getLogger(__name__)


@app.command()
def reset():
    reset_db()
    logger.debug('Удалили базу!')

@app.command()
def create():
    create_db()
    logger.debug('Создали базку!')


@app.command()
def add_test_rss():
    data = Path('weedly/db/test_rss.json').read_bytes()
    feeds = orjson.loads(data)
    for feed in feeds:
        db_session.add(Feed(**feed))
        db_session.commit()

    logger.debug('добавили в БД тестовые rss!')


if __name__ == '__main__':
    app()
