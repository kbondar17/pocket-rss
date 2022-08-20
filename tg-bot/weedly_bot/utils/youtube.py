import logging
import re
from typing import Optional

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class YoutubService:

    def extract_channel_id(self, text: str) -> Optional[str]:
        """Excract channel id from user input string.

        The function gets youtube urls, channel ids, playlist ids
        and converts them into the proper standard ID form:
        "UC...." or "UU...." (24 characters string); or "PL...." (34 character string)
        """
        return self._from_pattern(text) or self._from_page(text)

    def _from_page(self, text: str) -> Optional[str]:
        try:
            yt_content = httpx.get(text.strip()).content
            soup = BeautifulSoup(yt_content, 'html.parser')
            channel_url = soup.select_one("link[rel='canonical']").get('href')
            channel_id = channel_url.split('/')[-1]
            if channel_id != 'null' and channel_url != text:
                return channel_id

            channel_tag = soup.select_one("meta[itemprop='channelId']")
            return channel_tag.get('content')
        except ValueError:
            return None

    def _from_pattern(self, text: str) -> Optional[str]:
        patterns = [
            re.compile('U[UC][^&=]{22}'),
            re.compile('PL[^&=]{32}'),
            re.compile('RD[^&=]{41}'),
        ]
        for pattern in patterns:
            my_search = pattern.search(text)
            if my_search:
                break

        if my_search:
            proper_yt_id = my_search.group()
            return re.sub('^UU', 'UC', proper_yt_id)

        return None


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    yt = YoutubService()
    # inputs = [
    #     'https://www.youtube.com/watch?v=pwbD-yva2Cg',
    #     'https://www.youtube.com/channel/UCFNfeiYmTZ0f9oFj13_Re3g',
    #     'https://www.youtube.com/c/NavalnyLiveChannel',
    #     'https://www.youtube.com/c/ntvru',
    #     'https://www.youtube.com/c/tvrain',
    #     'https://www.youtube.com/watch?v=PlBrgFe5Fhg&list=PLUh4W61bt_K78f3sc1iM3NMN0_RM0f9Cv',
    # ]

    inputs = ['https://www.youtube.com/watch?v=S0AwwvtwDyk&t=19s',
              'https://www.youtube.com/watch?v=Jn5y2QONZhM']

    for text in inputs:
        channel_id = yt.extract_channel_id(text)
        logging.info(channel_id)
