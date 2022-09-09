import httpx
from yarl import URL
from datetime import datetime

from rssparser.api.models import Author, Feed


class FeedClient:

    def __init__(self, url: URL) -> None:
        self.url = url

    def get_all_rss(self) -> list[Feed]:
        url = self.url / 'api/v1/feeds/'
        raw_feeds = httpx.get(str(url), params={'rss-only': '1'}).json()
        return [Feed(**article) for article in raw_feeds]

    def get_all(self):
        url = self.url / 'api/v1/feeds/'
        raw_feeds = httpx.get(str(url), params={'rss-only': '0'}).json()
        return [Feed(**article) for article in raw_feeds]

    def get_oldest_article_datetime(self, feed_id)->None|datetime:
        url = self.url / f'api/v1/feeds/{feed_id}/oldest'
        r = httpx.get(str(url))
        if r.status_code > 200:
            print(r)
        else:
            return r.json()

    def get_authors(self, uid: str) -> list[Author]:
        return []
