import csv
import logging
import time
from pathlib import Path

from weedly.db.models import Article
from weedly.db.session import db_session

logger = logging.getLogger(__name__)


def from_csv(filepath: Path):
    with open(filepath, 'r', encoding='utf-8') as fs:
        fields = [
            'name',
            'author',
            'url',
            'source_name',
            'published',
        ]
        reader = csv.DictReader(fs, fields, delimiter=';')
        return list(reader)


def save_data(filepath: Path):
    data = from_csv(filepath)
    db_session.bulk_insert_mappings(Article, data)
    db_session.commit()


if __name__ == '__main__':
    start = time.time()
    filepath = Path('.data') / 'fake' / 'fakenews.csv'
    save_data(filepath)
    logger.info('Загрузка заняла: %s секунд.', time.time() - start)
