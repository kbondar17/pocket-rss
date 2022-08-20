from datetime import datetime
from typing import Optional, Any

from pydantic import AnyUrl, BaseModel, validator


class Model(BaseModel):
    uid: int

    class Config:
        orm_mode = True


class Feed(Model):
    name: str
    category: Optional[str]
    url: AnyUrl
    is_rss: bool


class User(Model):
    name: Optional[str]
    uid: int


class Author(Model):
    name: str
    feed_id: int


class Article(Model):
    title: str
    url: str
    published: datetime
    feed_id: int
    author_id: int
    feed: Optional[Any]
    description: Optional[str]

    @validator('feed')
    def get_feed_name(cls, value):
        return value.name

    class Config:
        arbitrary_types_allowed = True


class Channel(Model):
    title: str
    channel_id: str


class Video(Model):
    video_id: str
    title: str
    channel_id: str
    duration: Optional[str]
