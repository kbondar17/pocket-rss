from typing import Any

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from weedly.db.session import Base

db = SQLAlchemy()

users_n_feeds = Table(
    'users_n_feeds',
    Base.metadata,
    Column('user_id', ForeignKey('users.uid')),
    Column('feed_id', ForeignKey('feeds.uid')),
)


users_notificated_articles = Table(
    'users_notificated_articles',
    Base.metadata,
    Column('user_id', ForeignKey('users.uid')),
    Column('article_id', ForeignKey('articles.uid')),
)


feeds_to_notificate = Table(
    'feeds_to_notificate',
    Base.metadata,
    Column('user_id', ForeignKey('users.uid')),
    Column('feed_id', ForeignKey('feeds.uid')),
)


users_n_ytchannels = Table(
    'users_n_ytchannels',
    Base.metadata,
    Column('user_id', ForeignKey('users.uid')),
    Column('ytchannel_id', ForeignKey('channels.uid')),
)


class Feed(Base):
    """Класс для источников.

    Бывает двух видов: rss и НЕ-rss.
    Добавляется в БД через DataLoader.add_rss_feed и .add_not_rss_feed соответственно.

    feed_name берется из урла по принципу:
    (https://meduza.io/feature/2022/01/03/neizvestnyy-dvazhdy -> meduza.io)

    Уникальным должно быть сочетание feed_name + source_url.
    В БД могут быть разные source_url с одинаковыми feed_name
    (например, у Коммерсанта есть rss на разные темы)

    Атрибуты, доступные через relations:
    Feed.feed_authors - все авторы фида
    Feed.feed_articles - все статьи фида
    Feed.feed_subs - все юзеры, подписанные на фид
    """

    __tablename__ = 'feeds'

    uid = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    category = Column(String)
    url = Column(String, unique=True)
    is_rss = Column(Boolean)

    is_deleted = Column(Boolean, default=False)

    __table_args__ = (
        UniqueConstraint(name, url),
    )

    def __repr__(self) -> str:
        return 'Feed: [{uid}] {name}-{url})'.format(
            uid=self.uid,
            name=self.name,
            url=self.url,
        )


class User(Base):
    __tablename__ = 'users'

    uid = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    feeds: Any = relationship(
        'Feed',
        secondary='users_n_feeds',
        backref='feed_subs',
    )

    feeds_with_notifications: Any = relationship(
        'Feed',
        secondary='feeds_to_notificate',
        backref='feed_subs_notifications',
    )

    yt_channels: Any = relationship(
        'Channel',
        secondary='users_n_ytchannels',
        backref='channel_subs',
    )

    is_deleted = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return f'User: [{self.uid}] {self.name}'


class Author(Base):
    __tablename__ = 'authors'
    uid = Column(Integer, primary_key=True)
    name = Column(String)

    feed_id = Column(Integer, ForeignKey(Feed.uid))
    feed: Any = relationship(
        'Feed',
        foreign_keys=[feed_id],
        backref='feed_authors',
    )

    is_deleted = Column(Boolean, default=False)

    __table_args__ = (
        UniqueConstraint(name, feed_id),
    )

    def __repr__(self):
        return f'Author: [{self.uid}] {self.name}'


class Article(Base):
    __tablename__ = 'articles'

    uid = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    published = Column(DateTime)
    description = Column(String)
    feed_id = Column(Integer, ForeignKey(Feed.uid))
    feed: Any = relationship(
        'Feed',
        foreign_keys=[feed_id],
        backref='feed_articles',
    )

    author_id = Column(Integer, ForeignKey(Author.uid), index=True)
    author: Any = relationship(
        'Author',
        foreign_keys=[author_id],
        backref='author_articles',
    )

    notificated_users: Any = relationship(
        'User',
        secondary='users_notificated_articles',
        backref='receivied_articles',
    )

    is_deleted = Column(Boolean, default=False)

    __table_args__ = (
        UniqueConstraint(url, author_id),
    )

    def __repr__(self) -> str:
        return f'Article: [{self.uid}] {self.title}'


class Channel(Base):
    __tablename__ = 'channels'

    uid = Column(Integer, primary_key=True)
    title = Column(String)
    channel_id = Column(String, unique=True)
    is_deleted = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return f'Channel: [{self.uid}] {self.title}, {self.channel_id}'


class Video(Base):
    __tablename__ = 'videos'

    uid = Column(Integer, primary_key=True)
    video_id = Column(String, unique=True)
    title = Column(String)
    channel_id = Column(String, ForeignKey(Channel.channel_id))
    duration = Column(String, nullable=True)
    is_deleted = Column(Boolean, default=False)
    channel_videos: Any = relationship('Channel', backref='channel_videos')

    def __repr__(self) -> str:
        return f'Video: [{self.uid}] {self.video_id}, {self.title}'
