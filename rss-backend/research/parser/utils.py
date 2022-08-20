import re
import feedparser
import arrow
from datetime import datetime


def parse_rss(url):
    '''приводит данные из rss-потока в наш формат
       {'title': '',
            'author': '',
            'url': '',
            'source_name': '',
           'published': '' }
    '''
    content = feedparser.parse(url)
    articles = content['entries']
    result = []
    for article in articles:
        # проверка есть ли автор. если нет - оставляем название источника
        if 'author' in article.keys():
            author = article['author']
        else:
            author = get_name_from_url(url)
        if 'published' not in article.keys():
            published = arrow.now().timetuple()[:6]
        else:
            published = list(article['published_parsed'])[:6]

        link = article['link']
        title = article['title']
        source_name = get_name_from_url(url)
        result.append({
            'title': title,
            'author': author,
            'url': link,
            'source_name': source_name,
            'published': published,
        })

    return result



def get_name_from_url(url):
    name = re.findall(pattern='https://.*/', string=url)
    name = re.sub('https://', '', name[0])
    name = re.sub('www.', '', name)
    name = re.findall(pattern='.*/', string=name)
    name = name[0].strip('/')
    name = name.split('/')[0]
    return name
    # '''получает feed_name  из урла по принципу:
    #     (https://meduza.io/feature/2022/01/03/neizvestnyy-dvazhdy -> meduza.io)
    # '''

    # if 'www' in url:
    #     name =  re.findall(pattern='\.[a-z]*.[a-z]*', string= url)
    #     return name[0].strip('.')
    # name = re.findall(pattern='[a-z]*\.[a-z]*', string= url)
    # return name[0].strip('.')


def check_if_valid_rss(url):
    '''валидирует rss фид'''

    res = feedparser.parse(url)
    try:
        if res.bozo:
            print('неправильный rss ---', url)
            return False
        if res.status != 200:
            print('не удалось подключиться к rss ---', res.status)
            return False

    except Exception as ex:
        print('ошибка с rss ---', ex)

    else:
        print(f'{url} - валидный rss')
        return True


def datetime_parser(date):
    if type(date) == list:
        return datetime(*date)
    elif type(date) == str:
        return arrow.get(date).datetime
