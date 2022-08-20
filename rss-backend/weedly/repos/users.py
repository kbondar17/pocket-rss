from typing import Optional
import logging
from sqlalchemy.orm import Session

from weedly.db.models import Article, Channel, Feed, User
from weedly.db.session import db_session
from weedly.services.youtube import YoutubService
from weedly.errors import AlreadyExistsError, NotFoundError



class UserRepo:

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, uid: int, name: Optional[str]) -> User:
        query = self.session.query(User)
        user = query.filter_by(uid=uid).first()
        if user and user.is_deleted:
            user.is_deleted = False
            self.session.commit()

        if not user:
            user = User(uid=uid, name=name)
            self.session.add(user)
            self.session.commit()

        return user

    def get_by_id(self, uid: int) -> User:
        query = self.session.query(User)
        query = query.filter_by(uid=uid)
        query = query.filter_by(is_deleted=False)
        user = query.first()
        if not user:
            raise NotFoundError('user', uid)

        return user

    def get_all(self, limit: int = 100, offset=0) -> list[User]:
        query = self.session.query(User)
        query = query.filter_by(is_deleted=False)
        query = query.limit(limit).offset(offset)
        return query.all()

    def add_rss_to_user(self, uid: int, feed_id: int) -> list[Feed]:
        query = self.session.query(User)
        query = query.filter_by(uid=uid)
        query = query.filter_by(is_deleted=False)
        user = query.first()

        if not user:
            raise NotFoundError('user', uid)

        query = self.session.query(Feed)
        feed = query.filter_by(uid=feed_id, is_deleted=False).first()
        if not feed:
            raise NotFoundError('feeds', feed_id)

        user.feeds.append(feed)

        self.session.commit()
        return user.feeds

    def delete_rss_from_subs(self, uid: int, feed_id: int) -> list[Feed]:
        query = self.session.query(User)
        query = query.filter_by(uid=uid)
        query = query.filter_by(is_deleted=False)
        user = query.first()
        if not user:
            raise NotFoundError('user', uid)

        updated_feeds = [feed for feed in user.feeds if feed.uid != feed_id]
        if user.feeds == updated_feeds:
            raise NotFoundError('юзер не подписан на этот фид', uid)

        user.feeds = updated_feeds
        self.session.commit()
        return user.feeds

    def get_user_rss(self, uid) -> list[Feed]:
        query = self.session.query(User)
        query = query.filter_by(uid=uid)
        query = query.filter_by(is_deleted=False)
        user = query.first()
        if not user:
            raise NotFoundError('user', uid)

#        feeds = [feed for feed in user.feeds if not feed.is_deleted]

        return user.feeds

    def get_not_notificated_articles(self, user_id) -> list[Article]:
        query = self.session.query(User)
        query = query.filter_by(uid=user_id)
        query = query.filter_by(is_deleted=False)
        user = query.first()
        if not user:
            raise NotFoundError('user', user_id)

        all_not_notificated_articles = []

        # TODO: зарефачить этот водопад :)
        # if not
        if user.feeds_with_notifications:
            for feed in user.feeds_with_notifications:
                for article in feed.feed_articles:
                    notificated_users = [user.uid for user in article.notificated_users]
                    if user_id not in notificated_users:
                        all_not_notificated_articles.append(article)
                        article.notificated_users.append(user)
                        self.session.commit()

        return all_not_notificated_articles

    def add_yt_channel_to_user(self, user_id, yt_link) -> Channel:
        query = self.session.query(User)
        query = query.filter_by(uid=user_id)
        user = query.first()
        if not user:
            raise NotFoundError('user', user_id)
        yt = YoutubService()
        yt_channel_id = yt.extract_channel_id(yt_link)

        query = self.session.query(Channel)
        query = query.filter_by(channel_id=yt_channel_id)
        channel = query.first()

        if not channel:
            channel = Channel(title='Хз откуда брать название канала', channel_id=yt_channel_id)
            user.yt_channels.append(channel)

            self.session.add(channel)
            self.session.commit()
            return channel

        user.yt_channels.append(channel)
        self.session.commit()
        return channel

    def get_user_notifications(self, user_id) -> list[Feed]:
        query = self.session.query(User)
        query = query.filter_by(uid=user_id)
        user = query.first()
        if not user:
            raise NotFoundError('user', user_id)
        feeds = user.feeds_with_notifications
        if not feeds:
            raise NotFoundError('no notifications for user', user_id)
        return feeds

    def turn_on_notifications(self, user_id, feed_id) -> bool:
        query = self.session.query(User)
        query = query.filter_by(uid=user_id)
        user = query.first()
        if not user:
            raise NotFoundError('user', user_id)

        query = self.session.query(Feed)
        query = query.filter_by(uid=feed_id)
        feed = query.first()
        if not feed:
            raise NotFoundError('feed', feed_id)

        user.feeds_with_notifications.append(feed)
        self.session.commit()
        logging.debug('добавили юзеру %s нотификейшн для %s', user_id, feed_id)
        return True

    def turn_off_notifications(self, user_id, feed_id) :
        query = self.session.query(User)
        query = query.filter_by(uid=user_id)
        user = query.first()
        if not user:
            raise NotFoundError('user', user_id)

        query = self.session.query(Feed)
        query = query.filter_by(uid=feed_id)
        feed = query.first()
        if not feed:
            raise NotFoundError('feed', feed_id)

        user.feeds_with_notifications = [
            user_feed for user_feed in user.feeds_with_notifications if user_feed != feed]
        self.session.commit()
        return True

    def delete(self, uid: int) -> None:
        query = self.session.query(User)
        query = query.filter_by(uid=uid)
        user = query.first()
        if not user:
            raise NotFoundError('user', uid)

        user.is_deleted = True
        self.session.commit()
