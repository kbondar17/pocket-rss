import http
import logging

from flask import Blueprint, jsonify, request

from weedly import schemas
from weedly.db.session import db_session
from weedly.repos.users import UserRepo

routes = Blueprint('users', __name__)

repo = UserRepo(session=db_session)


@routes.get('/')
def get_all():
    entities = repo.get_all()
    users = [schemas.User.from_orm(entity).dict() for entity in entities]
    logging.debug('users----%s', users)
    return jsonify(users), http.HTTPStatus.OK


@routes.get('/<int:uid>')
def get_by_id(uid: int):
    entity = repo.get_by_id(uid)
    user = schemas.User.from_orm(entity)
    return user.dict(), http.HTTPStatus.OK


@routes.post('/')
def add():
    payload = request.json
    if not payload:
        return {'error': 'payload required'}, http.HTTPStatus.BAD_REQUEST

    user = schemas.User(**payload)
    entity = repo.add(name=user.name, uid=user.uid)
    new_user = schemas.User.from_orm(entity)
    return new_user.dict(), http.HTTPStatus.OK


@routes.post('/<int:uid>/feeds/')
def add_rss_to_user(uid: int):
    payload = request.json
    if not payload:
        return {'error': 'payload required'}, http.HTTPStatus.BAD_REQUEST

    feed_id = payload['feed_id']

    entities = repo.add_rss_to_user(uid=uid, feed_id=feed_id)
    feeds = [schemas.Feed.from_orm(entity).dict() for entity in entities]

    return jsonify(feeds), http.HTTPStatus.OK


@routes.get('/<int:uid>/notifications')
def get_notificated_feeds(uid):
    entities = repo.get_user_notifications(uid)
    feeds = [schemas.Feed.from_orm(entity).dict() for entity in entities]

    return jsonify(feeds), http.HTTPStatus.OK


@routes.put('/<int:uid>/feeds/<int:feed_id>/notification-on')
def turn_on_notifications(uid, feed_id):
    update_result = repo.turn_on_notifications(uid, feed_id)
    if update_result:
        return {}, http.HTTPStatus.OK


@routes.put('/<int:uid>/feeds/<int:feed_id>/notification-off')
def turn_off_notifications(uid, feed_id):
    update_result = repo.turn_off_notifications(uid, feed_id)
    if update_result:
        return {}, http.HTTPStatus.OK


@routes.delete('/<int:uid>/feeds/<int:feed_id>')
def delete_rss(uid, feed_id):
    entities = repo.delete_rss_from_subs(uid, feed_id)
    feeds = [schemas.Feed.from_orm(entity).dict() for entity in entities]
    return jsonify(feeds), http.HTTPStatus.OK


@routes.get('/<int:uid>/feeds/')
def get_user_feeds(uid: int):
    entities = repo.get_user_rss(uid)
    feeds = [schemas.Feed.from_orm(entity).dict() for entity in entities]
    return jsonify(feeds), http.HTTPStatus.OK


@routes.get('/<int:uid>/articles/')
def get_not_notificated_articles(uid: int):
    entities = repo.get_not_notificated_articles(uid)
    articles = [schemas.Article.from_orm(article).dict() for article in entities]
    return jsonify(articles), http.HTTPStatus.OK


@routes.post('/<int:uid>/yt-channels')
def add_yt_channels_to_user(uid):
    payload = request.json
    if not payload:
        return {'error': 'payload required'}, http.HTTPStatus.BAD_REQUEST

    yt_link = payload['yt_link']
    entity = repo.add_yt_channel_to_user(uid, yt_link)
    new_user_channel = schemas.Channel.from_orm(entity).dict()
    return new_user_channel, http.HTTPStatus.OK


@routes.delete('/<int:uid>')
def delete(uid: int):
    repo.delete(uid)
    return {}, http.HTTPStatus.NO_CONTENT
