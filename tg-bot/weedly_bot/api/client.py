from yarl import URL

from weedly_bot.api.feeds import FeedClient
from weedly_bot.api.authors import AuthorClient
from weedly_bot.api.users import UserClient
from weedly_bot.api.youtube import YoutubeClient


class ApiClient:

    def __init__(self, url: URL) -> None:
        self.feeds = FeedClient(url)
        self.authors = AuthorClient(url)
        self.users = UserClient(url)
        self.youtube = YoutubeClient(url)
        self.api_url = url
