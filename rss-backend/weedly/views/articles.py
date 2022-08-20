from http import HTTPStatus

from flask import Blueprint, abort, request

from weedly import schemas
from weedly.db.session import db_session
from weedly.jsonify import jsonify
from weedly.repos.articles import ArticleRepo

routes = Blueprint('articles', __name__)

repo = ArticleRepo(db_session)


@routes.get('/')
def get_all():
    feedname = request.args.get('feedname')
    if feedname:
        entities = repo.get_by_feed_name(feedname)
    else:
        entities = repo.get_all()

    articles = [schemas.Article.from_orm(ent).dict() for ent in entities]
    return jsonify(articles), 200


@routes.get('/<int:uid>')
def get_by_id(uid: int):
    entity = repo.get_by_id(uid)
    article = schemas.Article.from_orm(entity).dict()
    return jsonify(article), 200


@routes.post('/')
def add():
    payload = request.json
    if not payload:
        abort(HTTPStatus.BAD_REQUEST, 'payload required')
    payload['uid'] = -1

    article = schemas.Article(**payload)
    entity = repo.add(
        title=article.title,
        url=article.url,
        published=article.published,
        feed_id=article.feed_id,
        author_id=article.author_id,
    )
    new_article = schemas.Article.from_orm(entity).dict()
    return jsonify(new_article), HTTPStatus.CREATED
