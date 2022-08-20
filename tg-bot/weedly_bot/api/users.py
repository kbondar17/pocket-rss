from typing import Optional

import httpx

from yarl import URL
import requests
import logging


class UserClient:

    def __init__(self, url: URL) -> None:
        self.url = url

    def test(self):
        return 'its a uset test!!!'

    def add_user(self, uid, name):
        data = {"uid": uid, "name": name}

        url = self.url / 'api/v1/users/'
        try:
            req = httpx.post(str(url), json=data)  # .json()
            req.raise_for_status()
            logging.debug(f'Добавили юзера {uid} в БД')
        except httpx.HTTPError as er:
            logging.warning(er)
            logging.warning(f'Видимо, юзер %s уже существует', uid)

    def subscrbe_user_to_rss(self, uid, feed_id):
        """добавить rss в подписки юзера"""

        logging.debug('подисываем юзера %s на фид %s', uid, feed_id)
        data = {"feed_id": feed_id}
        url = self.url / 'api/v1/users/' / str(uid) / 'feeds/'
        print('вошли в подписывание')
        try:
            req = httpx.post(str(url), json=data, follow_redirects=True)
            print('обновленные подписки юзера')
            print(req.json())
            # logging.debug('обновленные подписки юзера --- %s',
            #               req.json()['updated_feeds'])
            # req.raise_for_status()
            return True

        except httpx.HTTPError as er:
            logging.warning(er)

    def get_user_notifications(self, uid):
        url = self.url / 'api/v1/users/' / str(uid) / 'notifications'
        try:
            req = httpx.get(str(url))
            req.raise_for_status()
            logging.debug('послали гет на %s', str(url))
            feeds = req.json()
            return feeds
        except httpx.HTTPStatusError as ex:
            logging.debug('у юзера нет уведомлений')
            return False

    def turn_on_notifications_for_feed(self, uid, feed_id):
        url = self.url / 'api/v1/users/' / \
            str(uid) / 'feeds/' / str(feed_id) / 'notification-on'
        try:
            req = httpx.put(str(url))
            logging.debug('отправили put запрос на %s', str(url))
            req.raise_for_status()
            return True
        except httpx.HTTPError as er:
            logging.warning(er)

    def turn_off_notifications_for_feed(self, uid, feed_id):
        url = self.url / 'api/v1/users/' / \
            str(uid) / 'feeds/' / str(feed_id) / 'notification-off'
        try:
            req = httpx.put(str(url))
            logging.debug('отправили put запрос на %s', str(url))
            req.raise_for_status()
            return True
        except httpx.HTTPError as er:
            logging.warning(er)

    def get_user_feeds(self, uid):
        '''[
            {
                "category": null,
                "is_rss": true,
                "name": "vc.ru",
                "uid": 4,
                "url": "https://vc.ru/rss?ref=vc.ru"
            },'''

        url = self.url / 'api/v1/users/' / str(uid) / 'feeds'

        try:
            req = httpx.get(str(url), follow_redirects=True)
            logging.debug('получили фиды от юзера --- %s', req.json())
            req.raise_for_status()
            return req.json()

        except httpx.HTTPError as er:
            logging.warning(er)

    def unsubcribe_user_from_rss(self, user_id, feed_id):
        url = self.url / 'api/v1/users/' / \
            str(user_id) / 'feeds' / str(feed_id)
        logging.debug('httpx.del --- %s', url)
        try:

            req = requests.delete(url)
            req.raise_for_status()
            logging.debug('удалили юзеру %s фид %s', user_id, feed_id)
            return True

        except httpx.HTTPError as er:
            logging.warning(er)

    def get_user_new_articles(self, user_id):
        url = self.url / 'api/v1/users/' / \
            str(user_id) / 'articles/'

        try:
            logging.debug('послали get на %s', url)
            res = requests.get(url, params={'not-notificated-only': '1'})
            res.raise_for_status
            if res.status_code == 200:

                articles = res.json()
                return articles

        except httpx.HTTPError as er:
            logging.warning(er)
            return None

    def get_all_users(self):
        url = self.url / 'api/v1/users'
        try:
            logging.debug('послали get на %s', url)
            res = requests.get(url)
            res.raise_for_status
            users = res.json()
            logging.debug('получили юзеров %s', users)
            return users

        except httpx.HTTPStatusError as er:
            logging.warning(er)
