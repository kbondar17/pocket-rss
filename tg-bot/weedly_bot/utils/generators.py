from aiogram.types import InlineKeyboardButton

from weedly_bot.utils.paginator import InlineKeyboardPaginator
import logging

logger = logging.getLogger(__name__)


class KeyboardGenerator:

    @staticmethod
    def chunks(lst, n):
        """нарезать список на равные куски (для пагинации)"""
        result = []
        for i in range(0, len(lst), n):
            result.append(lst[i:i + n])
        return result

    def generate_articles(self, list_of_articles, feed_name, data_for_return,
                          data_for_pagination, current=1):
        """все статьи фида, разбитые на сообщения с пагинацией"""

        logger.debug('получили в generate_articles %s, %s, %s,',
                     list_of_articles, data_for_return, data_for_pagination)

        for i, e in enumerate(list_of_articles):
            e['num'] = i + 1

        list_of_articles = self.chunks(list_of_articles, 4)

        numered_keyboard = {}
        for i, e in enumerate(list_of_articles):
            numered_keyboard[i + 1] = e

        kb = InlineKeyboardPaginator(max(numered_keyboard.keys()), current_page=current,
                                     data_pattern=data_for_pagination)

        if type(data_for_pagination) == str:
            kb = InlineKeyboardPaginator(max(numered_keyboard.keys()), current_page=current,
                                         data_pattern=data_for_pagination+'#{page}')

        text = f'Источник: {feed_name} \n\n'
        for i, e in enumerate(numered_keyboard[current]):
            text += f'{e["num"]}. <b>{e["title"]}</b> \n {e["url"]}\n\n '

        kb.add_after(InlineKeyboardButton(
            text='Назад', callback_data=data_for_return))

        return text, kb.markup

    def generate_feeds(self, feeds, data_for_return, action_for_calldata,
                       feeds_calldata, data_for_pagination, current=1):
        """ Все фиды, на которые подписан автор в виде инлайн клавы с пагинацией"""

        logging.debug(
            f'вошли в generate_feeds---- {feeds}, {data_for_return}, {data_for_pagination}')

        feeds_buttons = []

        for feed in feeds:
            print('feed---', feed)
            feed_calldata = feeds_calldata.new(action=action_for_calldata,
                                               feed_name=feed['name'].replace('&', ''), feed_id=feed['uid'], page=1)
            button = InlineKeyboardButton(
                text=feed['name'], callback_data=feed_calldata)
            feeds_buttons.append(button)

        feeds_buttons = self.chunks(feeds_buttons, 4)
        print('feeds_buttons---', feeds_buttons)
        # пронумерованная клава
        numered_keyboard = {}
        for i, e in enumerate(feeds_buttons):
            numered_keyboard[i + 1] = e

        feeds_keyboard = InlineKeyboardPaginator(max(numered_keyboard.keys(
        )), current_page=current, data_pattern=data_for_pagination+'#{page}')

        print('feeds_keyboard---', feeds_keyboard)
        for but in numered_keyboard[current]:
            feeds_keyboard.add_before(but)

        feeds_keyboard.add_after(InlineKeyboardButton(
            text='Назад', callback_data=data_for_return))

        print('feeds_keyboard с кнопкой возврата---', feeds_keyboard)

        logging.debug('клава на выходе генератора --- %s',
                      feeds_keyboard.markup)
        return feeds_keyboard.markup
