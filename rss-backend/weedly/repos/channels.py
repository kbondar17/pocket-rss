import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from weedly.db.models import Channel
from weedly.errors import AlreadyExistsError, NotFoundError

logger = logging.getLogger(__name__)


class ChannelRepo:

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, title: str, channel_id: str) -> Channel:
        try:
            channel = Channel(title=title, channel_id=channel_id)
            self.session.add(channel)
            self.session.commit()
            return channel
        except IntegrityError as err:
            raise AlreadyExistsError(entity='channels', constraint=str(err))

    def get_by_uid(self, uid: int) -> Channel:
        query = self.session.query(Channel)
        query = query.filter_by(uid=uid)
        channel = query.first()
        if not channel:
            raise NotFoundError('channel', uid)
        return channel

    def get_by_channel_id(self, channel_id: str) -> Channel:
        query = self.session.query(Channel)
        query = query.filter_by(channel_id=channel_id)
        channel = query.first()
        if not channel:
            raise NotFoundError('channel', channel_id)
        return channel

    def delete(self, uid: int) -> None:
        query = self.session.query(Channel)
        query = query.filter_by(uid=uid, is_deleted=False)
        channel = query.first()
        if not channel:
            raise NotFoundError('channel', uid)

        channel.is_deleted = True
        self.session.commit()
        logger.debug('Удалили Channel %S', channel)

    def get_all(self, limit: int = 100, offset=0) -> list[Channel]:
        query = self.session.query(Channel)
        query = query.filter_by(is_deleted=False)
        query = query.limit(limit).offset(offset)
        return query.all()
