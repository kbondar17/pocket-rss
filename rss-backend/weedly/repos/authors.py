import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from weedly.db.models import Article, Author, Feed
from weedly.errors import AlreadyExistsError, NotFoundError

logger = logging.getLogger(__name__)


class AuthorRepo:

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, name: str, feed_id, is_deleted=False) -> Author:
        new_author = Author(name=name, feed_id=feed_id, is_deleted=is_deleted)

        try:
            self.session.add(new_author)
            self.session.commit()
        except IntegrityError as err:
            raise AlreadyExistsError(entity='authors', constraint=str(err))

        logger.debug('Author %s добавлен в БД', name)

        return new_author

    def get_by_id(self, uid) -> Author:
        query = self.session.query(Author)
        query = query.filter_by(uid=uid)
        query = query.filter_by(is_deleted=False)
        feed = query.first()
        if not feed:
            raise NotFoundError('feed', uid)

        return feed

    def get_all_author_articles(self, uid) -> list[Article]:
        query = self.session.query(Author)
        query = query.filter_by(uid=uid)
        author = query.filter_by(is_deleted=False).first()

        if not author:
            raise NotFoundError('author', uid)

        articles = author.author_articles

        if not articles:
            raise NotFoundError('articles', uid)

        return articles

    def get_author_feed(self, uid) -> Feed:
        query = self.session.query(Author)
        query = query.filter_by(uid=uid)
        query = query.filter_by(is_deleted=False)
        author = query.first()

        if not author:
            raise NotFoundError('author', uid)

        feed = author.feed

        if not feed:
            raise NotFoundError('feed', uid)

        return feed
