from typing import Optional

import arrow
import httpx
import structlog
from yarl import URL


logger = structlog.getLogger(__name__)


class ArticleClient:

    def __init__(self, url: URL) -> None:
        self.url = url

    def add(
        self, feed_id: int, url: str, title: str,
        description: Optional[str],
        author_id: Optional[int], published: arrow.Arrow,
    ) -> None:

        payload = {'title': title, 'url': url,
                   'published': published.for_json(), 'feed_id': feed_id,
                   'author_id': author_id, 'description': description,
                   }

        api_url = self.url / 'api/v1/articles/'

        try:
            req = httpx.post(str(api_url), json=payload)
            req.raise_for_status()

        except httpx.HTTPStatusError:
            logger.warning('Статья уже в БД')
            return None


