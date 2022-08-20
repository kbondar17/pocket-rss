from aiogram.dispatcher.filters.state import StatesGroup, State

class My_states(StatesGroup):
    typing_name = State()
    typing_rss = State()
    send_youtube = State()