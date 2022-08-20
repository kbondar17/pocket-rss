import feedparser
import re
from pprint import pprint
import validators


def get_name_from_url(url):
    '''взяли из урла только название ресусра, чтобы написать юзеру, что на него подписались'''
    try:
        name = re.findall(pattern='https:\/\/.*\/|http:\/\/.*\/.*', string=url)
        name = re.sub('https://', '', name[0])
        name = re.sub('www.', '', name)
        name = re.findall(pattern='.*/', string=name)
        name = name[0].strip('/')
        name = name.split('/')[0]
        return name
    except Exception as ex:
        return url

def check_if_rss_is_working(url):
    '''пробуем парсить фид, если нет ошибки и есть статьи отдаем True'''
    feed = feedparser.parse(url)
    if feed['bozo']:
        print('ошибка подключени к rss')
        print(feed['bozo_exception'])
        return False

    if not feed['entries']:
        print('подключились к фиду, но в нем пусто')
        pprint(feed)
        return False

    return True


def check_if_valid_rss_url(url:str):
    '''Проверяем ок ли rss и добавляем в БД, если все ок'''
    url = url.strip()
    if not validators.url(url):
        return {'res': False,
                'msg': 'Неверный формат ссылки. Адрес должен быть таким -- https://meduza.io/rss/podcasts/tekst-nedeli'}

    elif not check_if_rss_is_working(url):
        return {'res': False,
                'msg': 'Не удается подключиться к этому rss фиду. Проверьте правильность написания или попробуйте позже'}
    else:

        source_name = get_name_from_url(url)
        return {'res': True,
                'msg': f'Работает! Добавили {source_name} в подписки!. '
                f'Через пару минут статьи появятся в разделе "Читать подписки"'}
