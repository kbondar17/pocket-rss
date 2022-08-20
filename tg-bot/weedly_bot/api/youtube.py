import logging
from typing import Optional

import httpx
from yarl import URL
import feedparser

from weedly_bot.utils.youtube import YoutubService


class YoutubeClient:

    def __init__(self, url: URL) -> None:
        self.url = url

    def get_user_subs(self):
        pass

    def get_yt_id_from_link(link) -> str:
        yt = YoutubService()
        yt_id = yt(link)
        return yt_id

    def test():
        return 'teeeeeeest'

    def get_rss_link_from_yt_link(self, url) -> str:
        print('вошли в get_rss_link_from_yt_link')
        yt = YoutubService()
        yt_id = yt.extract_channel_id(url)

        rss_link = f'https://www.youtube.com/feeds/videos.xml?channel_id={yt_id}'
        logging.debug(f'получилась rss ссылка {rss_link}')
        return rss_link

    def add_channel_to_bd_as_rss(self, yt_id):
        rss_link = f'https://www.youtube.com/feeds/videos.xml?channel_id={yt_id}'
        name = feedparser.parse(rss_link)['entries'][0]['author']

        data = {
            "name": name,
            "url": rss_link,
            "is_rss": True
        }

        try:

            url = self.url / 'api/v1/feeds/'
            logging.debug(f'послали post запрос на {str(url)}')
            res = httpx.post(str(url), json=data)
            res.raise_for_status
            logging.debug(f'добавили {name} в rss фиды')
            return True
        except httpx.HTTPStatusError as er:
            logging.debug(er)

    def subscribe_user_to_channel(self, u_id, channel):
        try:
            url = self.url / 'api/v1/users/' / str(u_id) / 'yt-channels'
            data = {'yt_link': channel}
            logging.debug('послали post на %s', url)
            req = httpx.post(str(url), json=data)
            req.raise_for_status
            logging.debug('подписали юзера %s на канал %s', u_id, channel)
            return True

        except httpx.HTTPError as er:
            logging.warning(er)
