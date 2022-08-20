import logging

import httpx
from yarl import URL

from weedly_bot.utils.rss import get_name_from_url

logger = logging.getLogger(__name__)


class FeedClient:

    def __init__(self, url: URL) -> None:
        self.url = url

    def get_all_smi_names(self):
        res = httpx.get(f'{str(self.url)}/api/v1/feeds/?rss-only=0').json()
        smi = [e['name'] for e in res]
        logger.debug('получили СМИ')
        logger.debug(res)
        return set(smi)

    def get_all_smi(self):
        res = httpx.get(f'{str(self.url)}/api/v1/feeds/?rss-only=0').json()
        logger.debug('получили СМИ')
        logger.debug(res)
        return res

    def get_all_articles_of_a_feed(self, feed_id):
        url = self.url / 'api/v1/feeds' / str(feed_id) / 'articles'
        res = httpx.get(str(url), follow_redirects=True).json()
        return res

    def get_all_authors_of_a_feed(self, media_name: str):
        media = media_name.replace('.', '-')
        res = httpx.get(
            f'{str(self.url)}/api/v1/feeds/source-name/{media_name}').json()
        logger.debug('вот авторы')
        # list of Author { "feed_id": 3, "name": "Рая Хачатрян", "uid": 12}
        logger.debug(res)

        return res

    def get_by_url(self, rss_url):
        data = {"url": rss_url}
        url = self.url / "api/v1/feeds" / "get-by-url/"

        try:
            res = httpx.post(str(url), json=data)
            logging.debug('послали post запрос на %s', str(url))

            res.raise_for_status()
            logger.debug('нашли фид по урлу --- %s', res.json())
            return res.json()

        except httpx.HTTPError as ex:
            logger.warning(ex)

    def add_rss_source(self, url, name=''):
        logger.debug('добавляем в бд --- %s', url)
        if not name:
            name = get_name_from_url(url)
        data = {"url": url, "is_rss": True, "name": name}

        try:
            url = self.url / 'api/v1/feeds/'
            req = httpx.post(str(url), json=data)  # .json()
            logging.debug('результат добавления фида %s', req)
            print(f'--- {req} ---')
            return req
        except httpx.HTTPError as ex:
            logger.warning(ex)
