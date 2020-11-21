from telegram import InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardMarkup
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
                       _(tr.HELP_WITH_LEARNING, context)],
                      ['Отзыв о преподователе']]
    return ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True
    )


def main_reply(reply, context):
    reply('Привет! Я бот!', reply_markup=get_main_keyboard(context))
