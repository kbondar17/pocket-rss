import time
from typing import Optional
import arrow

import structlog

from rssparser import rss
from rssparser.api.client import ApiClient
from rssparser.config import AppConfig

logger = structlog.getLogger(__name__)


class Worker:

    def __init__(self, config: AppConfig) -> None:
        self._is_working = False
        self._period = config.period
        self._client = ApiClient(config.api_url)
        self._feeds: dict[int, rss.Client] = {}

    def start(self) -> None:
        if self._is_working:
            return

        self._is_working = True
        while (self._is_working):
            logger.info('check feeds')

            self._work()

            logger.info('wait', timeout=self._period)
            time.sleep(self._period)

    def stop(self) -> None:
        self._is_working = False

    def _update_feeds(self) -> None:
        feeds = self._client.feeds.get_all_rss()

        # TODO: check deleted and modified feeds later
        for feed in feeds:

            # only add new feeds
            if feed.uid not in self._feeds:
                # TODO: last publish
                self._feeds[feed.uid] = rss.Client(feed.url)

    def _work(self) -> None:
        logger.info('check feeds and grab all of them')
        self._update_feeds()

        for feed_id, feed in self._feeds.items():
            self._load_feed(feed_id, feed)
    
    def get_oldest_feed_article(self, feed_id):
        oldest = self._client.feeds.get_oldest_article_datetime(feed_id)
        return oldest

    def _load_feed(self, feed_id: int, feed: rss.Client) -> None:
        logger.info('get rss from feed', feed=feed_id)
        try:
            articles = feed.parse()
            oldest = self.get_oldest_feed_article(feed_id)
            if oldest:
                articles = [e for e in articles if e.published > arrow.get(oldest) ]        

            for article in articles:
                author_id = self._get_author_id(feed_id, article.author)
                logger.debug('----добавляем статью----')
                logger.debug(article)

                self._client.articles.add(
                    feed_id=feed_id,
                    title=article.title,
                    description=article.description,
                    author_id=author_id,
                    url=article.link,
                    published=article.published
                )
        except AttributeError as ex:
            logger.warning(ex)
            print(feed)

    def _get_author_id(self, feed_id: int, name: Optional[str]) -> Optional[int]:
        if not name:
            return None

        author = self._client.authors.get_by_name(name, feed_id)
        if not author:
            author = self._client.authors.add(name, feed_id)

        return author.uid
