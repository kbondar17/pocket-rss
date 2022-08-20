from http import HTTPStatus

from flask import Blueprint, request

from weedly import schemas
from weedly.db.session import db_session
from weedly.jsonify import jsonify
from weedly.repos.channels import ChannelRepo

routes = Blueprint('channels', __name__)

repo = ChannelRepo(db_session)


@routes.get('/')
def get_all():
    args = request.args
    channel_id = args.get('channel_id')
    if channel_id:
        entity = repo.get_by_channel_id(channel_id)
        channel = schemas.Channel.from_orm(entity).dict()
        return jsonify([channel]), HTTPStatus.OK

    entities = repo.get_all()
    channels = [schemas.Channel.from_orm(entity).dict() for entity in entities]

    return jsonify(channels), HTTPStatus.OK


@routes.get('/<int:uid>')
def get_by_uid(uid):
    channel = repo.get_by_uid(uid)
    data = schemas.Channel.from_orm(channel).dict()
    return jsonify(data), HTTPStatus.OK


@routes.post('/')
def add():
    payload = request.json
    if not payload:
        return {'error': 'payload required'}, HTTPStatus.BAD_REQUEST

    payload['uid'] = 0
    channel = schemas.Channel(**payload)
    entity = repo.add(
        title=channel.title,
        channel_id=channel.channel_id,
    )
    new_channel = schemas.Channel.from_orm(entity)
    return jsonify(new_channel.dict()), HTTPStatus.CREATED


@routes.delete('/<int:uid>')
def delete(uid: int):
    repo.delete(uid)
    return {}, HTTPStatus.NO_CONTENT
