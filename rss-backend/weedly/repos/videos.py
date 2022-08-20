import logging
from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from weedly.db.models import Channel, Video
from weedly.errors import AlreadyExistsError, NotFoundError

logger = logging.getLogger(__name__)


class VideoRepo:

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(
        self,
        video_id: str,
        title: str,
        channel_id: str,
        duration: Optional[str],
    ) -> Video:
        try:
            video = Video(video_id=video_id, title=title, channel_id=channel_id, duration=duration)
            self.session.add(video)
            self.session.commit()
            return video
        except IntegrityError as err:
            raise AlreadyExistsError(entity='video', constraint=str(err))

    def get_by_id(self, uid: int) -> Video:
        query = self.session.query(Video)
        query = query.filter_by(uid=uid)
        query = query.filter_by(is_deleted=False)
        video = query.first()
        if not video:
            raise NotFoundError('video', uid)

        return video

    def get_by_video_id(self, video_id: str) -> Video:
        query = self.session.query(Video)
        query = query.filter_by(video_id=video_id)
        query = query.filter_by(is_deleted=False)
        video = query.first()
        if not video:
            raise NotFoundError('video', video_id)

        return video

    def get_by_channel_id(self, channel_id) -> list[Video]:
        query = self.session.query(Channel)
        channel = query.filter_by(channel_id=channel_id).first()

        if not channel:
            raise NotFoundError('channel_id', channel_id)

        return channel.channel_videos

    def get_all(self, limit: int = 100, offset=0) -> list[Video]:
        query = self.session.query(Video)
        query = query.filter_by(is_deleted=False)
        query = query.limit(limit).offset(offset)

        return query.all()

    def delete(self, uid: int) -> None:
        query = self.session.query(Video)
        query = query.filter_by(uid=uid)
        video = query.first()
        if not video:
            raise NotFoundError('video', uid)
        video.is_deleted = True
        self.session.commit()
