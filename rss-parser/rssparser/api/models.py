from typing import Optional
from arrow import Arrow

from pydantic import BaseModel


class Feed(BaseModel):
    uid: int
    url: str
    category: Optional[str]
    is_rss: bool
    name: str


class Article(BaseModel):
    uid: Optional[int]
    title: str
    url: str
    published: Arrow
    feed_id: int
    author_id: Optional[int]
    description: Optional[str]

    class Config:
        arbitrary_types_allowed = True


class Author(BaseModel):
    uid: int
    name: str
    feed_id: int
