from weedly_bot.paths.archive.search import dp
from .welcome_message import dp
from weedly_bot.paths.archive.search import dp
from .my_subs import dp
from .add_feeds import dp
from .notifications import dp

# импортируется в конце
from .echo import dp


__all__ = ['dp']
