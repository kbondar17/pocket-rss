from typing import Optional

import httpx
import structlog
from yarl import URL

from rssparser.api.models import Author

logger = structlog.getLogger(__name__)


class AuthorClient:

    def __init__(self, url: URL) -> None:
        self.url = URL(url)

    def get_by_name(self, name, feed_id: int) -> Optional[Author]:
        url = self.url / 'api/v1/feeds' / str(feed_id) / 'authors/'
        response = httpx.get(str(url))
        response.raise_for_status()
        payload = response.json()

        for author in payload:
            if author['name'] == name:
                return Author(**author)

        return None

    def get_by_id(self, author_id: int) -> Author:
        url = self.url / 'api/v1/authors/'
        response = httpx.get(str(url), params={'uid': author_id})
        response.raise_for_status()
        payload = response.json()
        return Author(**payload)

    def add(self, name, feed_id) -> Author:
        payload = {'name': name, 'feed_id': feed_id}
        url = self.url / 'api/v1/authors/'
        req = httpx.post(str(url), json=payload).json()
        logger.debug(f'Добавили: name - {name}, feed_id - {feed_id} .')
        return Author(**req)
