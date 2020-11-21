from telegram import InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardMarkup, CallbackQuery
import translations as tr
from translations import gettext as _


def make_inline_keyboard(rows):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text, callback_data=data) for text, data in row]
        for row in rows
    ])


def get_main_keyboard(context):
    reply_keyboard = [[_(tr.MENU_HELLO, context),
                       _(tr.MENU_SELECT_LANG, context)],
                      [_(tr.MENU_SEND_FEEDBACK, context),
                       _(tr.MENU_REVIEW, context)]]
    return ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True
    )


def main_reply(reply, context):
    reply(_(tr.GOT_TO_MAIN_MENU, context),
          reply_markup=get_main_keyboard(context))


def answer_query(update, context):
    query: CallbackQuery = update.callback_query
    data = query.data
    query.answer()
    return data, query.edit_message_text
