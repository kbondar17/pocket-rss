import logging
from pathlib import Path
from statistics import mode

import orjson
from typer import Typer

from weedly.db.models import Feed, Article
from weedly.db.session import db_session


def leave_newset_30():
    for feed in db_session.query(Feed):
        import time
        print('deleeting feeds', time.time())
        articles = feed.articles 
        if articles.count() > 30:
            first_30 = feed.articles.order_by(Article.published.desc()).slice(0,30)
            first_30 = [e.uid for e in first_30]
            to_delete = articles.filter(~Article.uid.in_(first_30))
            # count  = len(to_delete.all())
            count = to_delete.count()
            print(f'deletin {count} articles from {feed}')
            to_delete.delete()
            db_session.commit()
    
def test():
    
    for feed in db_session.query(Feed):
        # oldest_date_time = feed.articles.order_by(Article.published.asc()).first().published
        # print(feed, oldest_date_time)
        print(feed, feed.articles.count())

if __name__ == '__main__':
    leave_newset_30()
    test()
