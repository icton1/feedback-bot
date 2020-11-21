from telegram import InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardMarkup, CallbackQuery
import translations as tr
from translations import gettext as _


def make_inline_keyboard(tuples):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text, callback_data=data) for text, data in row]
        for row in tuples
    ], )


def get_main_keyboard(context):
    reply_keyboard = [[_(tr.HELLO, context)],
                      ['Обратиться в центр качества образования',
                       _(tr.CHANGE_LANG, context)],
                      ['Отзыв о преподователе']]
    return ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True
    )


def main_reply(reply, context):
    reply('Привет! Я бот!', reply_markup=get_main_keyboard(context))


def answer_query(update, context):
    query: CallbackQuery = update.callback_query
    data = query.data
    query.answer()
    return data, query.edit_message_text
