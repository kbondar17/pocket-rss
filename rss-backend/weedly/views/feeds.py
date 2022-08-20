from http import HTTPStatus

from flask import Blueprint, request

from weedly import schemas
from weedly.db.session import db_session
from weedly.jsonify import jsonify
from weedly.repos.feeds import FeedRepo
from weedly.errors import AlreadyExistsError, NotFoundError

routes = Blueprint('feeds', __name__)

repo = FeedRepo(db_session)


@routes.get('/')
def get_all():
    args = request.args
    rss_only = bool(int(args.get('rss-only', '0')))

    if rss_only:
        entities = repo.get_all_rss()
        feeds = [schemas.Feed.from_orm(entity).dict() for entity in entities]
        return jsonify(feeds), HTTPStatus.OK

    entities = repo.get_all()
    feeds = [schemas.Feed.from_orm(entity).dict() for entity in entities]
    return jsonify(feeds), HTTPStatus.OK


@routes.get('/<int:uid>')
def get_by_id(uid: int):
    feed = repo.get_by_id(uid)
    data = schemas.Feed.from_orm(feed).dict()
    return jsonify(data), HTTPStatus.OK


@routes.get('/source-name/<string:name>')
def get_by_source_name(name):
    entities = repo.get_authors_by_name(name)
    authors = [schemas.Author.from_orm(entity).dict() for entity in entities]
    return jsonify(authors), HTTPStatus.OK


@routes.get('/<int:uid>/authors/')
def get_authors(uid: int):
    entities = repo.get_authors_by_id(uid)
    authors = [schemas.Author.from_orm(entity).dict() for entity in entities]
    return jsonify(authors), HTTPStatus.OK


@routes.get('/<int:uid>/articles/')
def get_articles(uid):
    entities = repo.get_articles(uid)
    articles = [schemas.Article.from_orm(article).dict() for article in entities]
    return jsonify(articles), HTTPStatus.OK


@routes.post('/')
def add():
    payload = request.json
    print('payload---', payload)
    if not payload:
        return {'error': 'payload required'}, HTTPStatus.BAD_REQUEST

    payload['uid'] = 0
    feed = schemas.Feed(**payload)
    try:
        entity = repo.add(
            name=feed.name,
            url=feed.url,
            is_rss=feed.is_rss,
            category=feed.category,
        )

    except AlreadyExistsError:
        print('такой фид уже есть, отправляем 200')
        return 'Такой фид уже есть', 200

    if not entity:
        return {}, HTTPStatus.BAD_REQUEST

    new_feed = schemas.Feed.from_orm(entity)
    print('не поймали м')
    return new_feed.dict(), HTTPStatus.CREATED


@routes.put('/')
def update():
    payload = request.json
    if not payload:
        return {'error': 'payload required'}, HTTPStatus.BAD_REQUEST

    feed = schemas.Feed(**payload).dict()
    entity = repo.update(**feed)
    updated_feed = schemas.Feed.from_orm(entity).dict()

    return jsonify(updated_feed), HTTPStatus.OK


@routes.post('/get-by-url/')
def get_by_url():
    payload = request.json
    if not payload:
        return {'error': 'payload required'}, HTTPStatus.BAD_REQUEST

    url = payload['url']
    print('payload в гет бай урл---', payload)
    entity = repo.get_by_url(url)
    feed = schemas.Feed.from_orm(entity).dict()

    return jsonify(feed), HTTPStatus.OK


@routes.delete('/<int:uid>')
def delete(uid: int):
    repo.delete(uid)
    return '', HTTPStatus.NO_CONTENT
