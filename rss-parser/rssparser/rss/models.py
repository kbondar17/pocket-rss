import re
from datetime import datetime, timedelta
from typing import Optional
import logging
import pytz

import arrow
from pydantic import BaseModel, Field, root_validator, validator

logger = logging.getLogger(__name__)


def get_local_time():
    return datetime.now(pytz.timezone('Europe/Moscow'))


class Article(BaseModel):
    title: str
    link: str
    author: Optional[str]
    published: arrow.Arrow = Field(default_factory=get_local_time, alias='published_parsed')
    description: Optional[str]

    @validator('published', pre=True)
    def convert_data(cls, value):  # noqa: N805
        if isinstance(value, arrow.Arrow):
            return value

        return arrow.get(value) + timedelta(hours=3)

    @root_validator(pre=True)
    def get_name_from_source_name(cls, values):
        """вместо пустого автора вставляем название издания."""
        author = values.get('author')
        link = values.get('link')
        if not author:
            if 'www' in link:
                name = re.findall(pattern='\.[a-z]*.[a-z]*', string=link)
            else:
                name = re.findall(pattern='[a-z]*\.[a-z]*', string=link)
            values['author'] = name[0].strip('.')

        return values

    class Config:
        arbitrary_types_allowed = True
