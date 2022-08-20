import logging

import structlog

from rssparser.config import load_from_env
from rssparser.worker import Worker
from httpx import ConnectError
import backoff

logging.basicConfig(level=logging.DEBUG)

logger = structlog.getLogger(__name__)


@backoff.on_exception(backoff.expo,
                      ConnectError,
                      max_time=300)
def main():
    logger.info('start parser')
    config = load_from_env()
    worker = Worker(config)

    try:
        worker.start()
    
    except KeyboardInterrupt:
        logger.info('received stop signal')
        worker.stop()

    logger.info('stop parser')


if __name__ == '__main__':
    main()
