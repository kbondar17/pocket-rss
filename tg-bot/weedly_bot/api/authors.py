import httpx
from yarl import URL

import logging

logger = logging.getLogger(__name__)

# TODO: добавить отлов ошибок


class AuthorClient:

    def __init__(self, url: URL) -> None:
        self.url = url

    def get_articles_of_an_author(self, author_id: int):

        url = self.url / 'api/v1/authors' / author_id / 'articles/'
        req = httpx.get(str(url)).json()

        logger.debug('--- полученные статьи по айди автора %s ---', author_id)
        logger.debug(req)

        return req

    def get_author_feed(self, author_id: int):
        url = self.url / 'api/v1/authors' / author_id / 'feed'
        req = httpx.get(str(url)).json()

        logger.debug('получили фид автора')
        logger.debug(req)

        return req
