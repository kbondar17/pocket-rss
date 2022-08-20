import httpx
from yarl import URL

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

    def get_authors(self, uid: str) -> list[Author]:
        return []
