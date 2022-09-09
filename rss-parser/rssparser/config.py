import os
from dataclasses import dataclass

from yarl import URL


@dataclass
class AppConfig:
    api_url: URL
    period: int


def load_from_env() -> AppConfig:
    # url = URL('http://127.0.0.1:5000/')
    print('os.environ---',os.environ)
    url = URL(os.environ['API_URL'])
    return AppConfig(
        api_url=url,
        period=int(os.getenv('TASK_PERIOD', 20)),
    )
