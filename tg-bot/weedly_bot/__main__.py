import asyncio
import logging
from weedly_bot.loader import bot, api_client
from aiogram import executor
from weedly_bot.paths import dp


logger = logging.getLogger(__name__)


async def notificator():

    while True:
        print('зашли в нотификатор')
        ids = [user['uid'] for user in api_client.users.get_all_users()]
        print('ids---', ids)
        for id_ in ids:
            articles = api_client.users.get_user_new_articles(id_)
            print('articles---', articles)
            if articles:
                for article in articles[:3]:
                    print('попробовали отправить', article['title'])

                    # ДОБАВИТЬ ФИЛЬТР ПО ВРЕМЕНИ
                    text = f'<b>{article["title"]}</b>\n\nИсточник: {article["feed"]}\n{article["url"]}'
                    # f'
                    #     *{article["title"]}*\n\n
                    #      {article["feed"]}\n
                    #     {article["url"]}'

                    # text = f'Источник: {article["feed"]}\n\n{article["title"]}\n {article["url"]}'
                    await bot.send_message(text=text, chat_id=id_, disable_web_page_preview=True)
                    await asyncio.sleep(0.2)

        await asyncio.sleep(1)


if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    # loop.create_task(notificator())
    # asyncio.run(notificator())

    logger.error('окей лестгоу')
    executor.start_polling(dp)
