'''тут функции для обращения к БД'''

from weedly.db.models import Feed, Article, Author
from weedly.db.session import db_session
import research.parser.utils as utils


class DataGetter:
    '''Класс DataGetter используется для получения данных из БД'''

    @staticmethod
    def get_latest_news(how_many=3):
        '''последние n новостей, добавленные в БД'''

        res = db_session.query(Article).distinct(Article.title).order_by(Article.published.desc())[:how_many]
        return {'result': [e.title for e in res]}

    @staticmethod
    def get_articles_of_a_feed(feed_name) -> list:
        '''все статьи фида. ищем фид по имени (у одного feed_name может быть несколько ссылок)
        проходимся по ним и отдаем Articles в формате нашего стандартного словаря
        '''

        feeds = db_session.query(Feed).filter(Feed.feed_name.contains(feed_name)).all()
        result = []
        for feed in feeds:
            result.append(feed.feed_articles)
        result = [e for e in result if e][0]
        result = [
            {'title': e.title, 'author': e.author_name.author_name, 'url': e.url,
             'source_name': e.feed_name.feed_name, 'published': e.published} for e in result
        ]
        return result


    @staticmethod
    def get_all_feeds_names():
        '''все имена фидов из БД'''

        res = db_session.query(Feed.feed_name).distinct(Feed.feed_name).all()
        return [e.feed_name for e in res]

    @staticmethod
    def get_all_authors_of_a_feed(feed_name):
        '''все авторы фида'''

        feed = db_session.query(Feed).filter(Feed.feed_name.contains(feed_name)).all()
        authors = []
        for e in feed:
            authors.append(e.feed_authors)
        return [e for e in authors if e]


class DataLoader:
    '''Класс DataLoader используется для загрузки данных в БД.
    '''
    @staticmethod
    def add_rss_feed(source_url):
        '''добавляет rss фид в БД.
        1. проверяет корректность ссылки. если некорректная - выдает ошибку.
        2. если такой фид уже есть - отдает его экземпляр
        3. если такого фида нет - сначала добавляет в БД, а затем отдает экземпляр
        '''

        if not utils.check_if_valid_rss(source_url):
            raise ValueError('не валидный rss!')
        else:
            feed = db_session.query(Feed).filter(Feed.source_url == source_url)
            if feed.count():
                print(f'Такой feed уже есть. id == {feed.first().feed_id}')
                return feed.first()
            else:
                source_name = utils.get_name_from_url(source_url)
                new_rss = Feed(feed_name=source_name, source_url=source_url, is_rss_feed=True)
                db_session.add(new_rss)
                db_session.commit()
                print(f'добавили {source_url} в БД')
                return new_rss

    @staticmethod
    def add_not_rss_feed(source_url):
        '''добавляет НЕ rss feed в БД.
        если такой фид уже есть - отдает его экземпляр,
        если такого фида нет - сначала добавляет в БД, а затем отдает экземпляр.

        feed_name - домен фида (https://meduza.io/feature/2022/01/03/neizvestnyy -> meduza.io)
        '''

        feed_name = utils.get_name_from_url(source_url)
        feed = db_session.query(Feed).filter(Feed.feed_name == feed_name,
                                             Feed.is_rss_feed == False)
        if feed.count():  # проверяем на наличие
            print(f'Такой feed уже есть. id == {feed.first().feed_id}')
            return feed.first()
        new_rss = Feed(feed_name=feed_name, source_url=feed_name, is_rss_feed=False)  # добавляем, если нет
        db_session.add(new_rss)
        db_session.commit()
        print(f'добавили {source_url} в БД')
        return new_rss

    def add_author(self, author_name, url):
        '''Добавляет автора в БД.
        НА ВХОД : имя автора и ссылка на статью или источник.

        из урла берем имя фида (домен).
        если фида нет в БД - добавляем и получаем экземпляр Feed, если
        есть - просто получаем экземпляр Feed.

        НА ВЫХОД : если такой автор уже есть (сочетание имени и feed_id) - отдает его экземпляр,
                   если такого автора нет - сначала добавляет в БД, а затем отдает экземпляр.
        '''

        feed = self.add_not_rss_feed(url)
        author_from_bd = db_session.query(Author).filter(Author.author_name == author_name,
                                                         Author.feed_id == feed.feed_id)
        if author_from_bd.count():
            print(f'такой автор уже есть. id =={author_from_bd.first().author_id}')
            return author_from_bd.first()
        else:
            new_author = Author(author_name=author_name, feed_name=feed)
            db_session.add(new_author)
            db_session.commit()
            print(f'добавили {author_name} в БД!')
            return new_author

    def add_article(self, article: dict):
        '''добавляет статью в БД.
        НА ВХОД - словарь с данными о статье.
            {'title': '',
            'author': '',
            'url': '',
            'source_name': '',
      !!!   'published': list[2021,12,12,1,1,] или str('2021-12-12 00:00:00')} !!!

        если статья уже есть (сочетание урл + имя автора) отдает False.
        из урла берем имя фида (домен).
        если фида нет в БД - добавляем и получаем экземпляр Feed, если есть - просто получаем экземпляр Feed.
        если автора нет в БД - добавляем.
        НА ВЫХОД - сообщение о добавлении.
        '''

        # проверяем
        article_url_exists = db_session.query(Article).filter(Article.url == article['url'])
        authors_of_existing_article = [e.author_name.author_name for e in article_url_exists]
        if article_url_exists.count() and article['author'] in authors_of_existing_article:
            print(
                f'статья {article["title"]} уже в БД! ---- id == {article_url_exists.first().article_id}')
            return False

        else:
            # берем данные автора и фида
            author_data = self.add_author(article['author'], article['url'])
            feed_data = self.add_not_rss_feed(article['url'])
            print('add_article: author_data---', author_data)
            print('add_article: feed_data---', feed_data)

            # добавляем
            new_article = Article(title=article['title'], url=article['url'],
                                  published=utils.datetime_parser(article['published']),
                                  feed_id=feed_data.feed_id, feed_name=feed_data,
                                  author_id=author_data.author_id, author_name=author_data,
                                  is_deleted=False)
            db_session.add(new_article)
            db_session.commit()
            print(f'добавили статью {article["title"]} в БД!')
            return f'добавили статью {article["title"]} в БД!'
