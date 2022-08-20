from datetime import datetime
import logging

import feedparser
import httpx
import structlog
from tenacity import retry, TryAgain, stop_after_attempt, wait_fixed, after_log, retry_if_not_exception_type

from rssparser.rss.models import Article

logger = structlog.getLogger(__name__)


class Client:

    def __init__(self, url: str, last_published: datetime = None) -> None:
        self.url = url
        self.last_published = last_published

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(1),
        retry=retry_if_not_exception_type(httpx.RequestError),
        after=after_log(logger, logging.DEBUG))
    def parse(self) -> list[Article]:
        try:
            resp = httpx.get(self.url)
            resp.raise_for_status()
            feed = feedparser.parse(resp.text)
            articles = feed['entries']

            if not articles:
                raise ValueError(f'No articles in {self.url}')

            return [Article(**article) for article in articles]

        except Exception as ex:
            logger.warning(ex)
            raise TryAgain



