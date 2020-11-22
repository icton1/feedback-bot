import logging
from states import State
import translations as tr
from translations import gettext as _
from config import token
import learning_help
import teachers_review
import feedback
import utils
import filters
from random import choice

from telegram import Update, ReplyKeyboardMarkup, Message
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext, CallbackQueryHandler
)

POLL_STATE = 'POLL_STATE'
USED_BAD_WORDS = 'USED_BAD_WORDS'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def hello(update, context):
    update.effective_user.send_message(
        _(tr.HELLO_TEXT, context),
        reply_markup=utils.get_main_keyboard(context)
    )


def start(update: Update, context: CallbackContext):
    hello(update, context)
    return State.FIRST_NODE


def show_change_lang_prompt(reply, context):
    reply_keyboard = tr.LANGUAGES
    reply(_(tr.SELECT_LANG, context),
          reply_markup=utils.make_inline_keyboard(reply_keyboard))


def first_node(update: Update, context: CallbackContext):
    text = update.message.text
    if text == _(tr.MENU_REVIEW, context):
        return teachers_review.start(update, context)
    elif text == _(tr.MENU_HELLO, context):
        hello(update, context)
        return
    elif text == _(tr.MENU_SELECT_LANG, context):
        show_change_lang_prompt(update.effective_user.send_message, context)
        return State.CHANGE_LANG
    elif text == _(tr.MENU_SEND_FEEDBACK, context):
        return feedback.start(update, context)
    elif len(text) > 0 and text[-1] == '?':
        update.message.reply_text(_(tr.PASTA_STUDOFIS, context))


def choose_lang(update, context):
    data, reply = utils.answer_query(update, context)
    context.user_data['lang'] = data
    reply(_(tr.SUCCESSFULLY_SELECTED_LANG, context))
    utils.main_reply(update.effective_user.send_message, context)
    return State.FIRST_NODE


def send_bad_language(update, context):
    if context.user_data.setdefault(USED_BAD_WORDS, False):
        context.user_data[USED_BAD_WORDS] = True
        with open('pivo.jpg', 'rb') as photo:
            update.message.reply_photo(photo=photo)
    else:
        pic = choice(['pivo.jpg', 'mati_bad.jpg',
                      'no_mat_please.jpg', 'sticker_mati'])
        if pic == 'sticker_mati':
            pass
            # TODO update.message.reply_sticker()
        else:
            with open(pic, 'rb') as photo:
                update.message.reply_photo(photo=photo)


def main():
    updater = Updater(token, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(filters.BAD_WORDS, send_bad_language))

    main_conv = ConversationHandler(
        entry_points=[MessageHandler(Filters.text, start)],
        states={
            State.FIRST_NODE: [MessageHandler(Filters.text & ~Filters.command,
                                              first_node)],
            State.CHANGE_LANG: [CallbackQueryHandler(choose_lang)],
            **learning_help.get_states(),
            **teachers_review.get_states(),
            **feedback.get_states()
        },
        fallbacks=[CommandHandler('stop', start)],
    )

    dispatcher.add_handler(main_conv)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
