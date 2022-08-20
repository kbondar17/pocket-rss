from http import HTTPStatus

from flask import Blueprint, abort, request

from weedly import schemas
from weedly.db.session import db_session
from weedly.jsonify import jsonify
from weedly.repos.videos import VideoRepo

routes = Blueprint('videos', __name__)

repo = VideoRepo(db_session)


@routes.get('/')
def get_all():
    args = request.args
    video_id = args.get('video_id')
    if video_id:
        entity = repo.get_by_video_id(video_id)
        video = schemas.Video.from_orm(entity).dict()
        return jsonify([video]), HTTPStatus.OK

    channel_id = args.get('channel_id')
    if channel_id:
        entities = repo.get_by_channel_id(channel_id)
        videos = [schemas.Video.from_orm(entity).dict() for entity in entities]
        return jsonify(videos), HTTPStatus.OK

    entities = repo.get_all()
    videos = [schemas.Video.from_orm(entity).dict() for entity in entities]
    return jsonify(videos), HTTPStatus.OK


@routes.get('/<int:uid>')
def get_by_uid(uid):
    video = repo.get_by_id(uid)
    data = schemas.Video.from_orm(video).dict()
    return jsonify(data), HTTPStatus.OK


@routes.post('/')
def add():
    payload = request.json
    if not payload:
        abort(HTTPStatus.BAD_REQUEST, 'payload required')
    payload['uid'] = 0
    video = schemas.Video(**payload)
    entity = repo.add(
        video_id=video.video_id,
        title=video.title,
        channel_id=video.channel_id,
        duration=video.duration,
    )
    new_video = schemas.Video.from_orm(entity).dict()
    return jsonify(new_video), HTTPStatus.CREATED


@routes.delete('/<int:uid>')
def delete(uid: int):
    repo.delete(uid)
    return {}, HTTPStatus.NOT_FOUND
