from http import HTTPStatus

from flask import Blueprint, abort, request

from weedly import schemas
from weedly.db.session import db_session
from weedly.jsonify import jsonify
from weedly.repos.authors import AuthorRepo

routes = Blueprint('authors', __name__)

repo = AuthorRepo(db_session)


@routes.post('/')
def add():
    payload = request.json
    if not payload:
        abort(HTTPStatus.BAD_REQUEST, 'payload required')

    payload['uid'] = 0

    author = schemas.Author(**payload)
    entity = repo.add(name=author.name, feed_id=author.feed_id)
    new_author = schemas.Author.from_orm(entity)
    return jsonify(new_author.dict()), HTTPStatus.CREATED


@routes.get('/<int:uid>')
def get_by_id(uid):
    entity = repo.get_by_id(uid)
    author = schemas.Author.from_orm(entity)
    return jsonify(author.dict()), 200


@routes.get('/<int:uid>/feed')
def get_author_feed(uid):
    entity = repo.get_author_feed(uid)
    feed = schemas.Feed.from_orm(entity)
    return jsonify(feed.dict()), 200


@routes.get('<int:uid>/articles/')
def get_all_articles_of_author(uid):
    entities = repo.get_all_author_articles(uid)
    articles = [schemas.Article.from_orm(article).dict() for article in entities]
    return jsonify(articles), 200
