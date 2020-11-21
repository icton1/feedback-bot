import logging
from states import State
import translations as tr
from translations import gettext as _
import learning_help
import teachers_review
import feedback
import utils

from telegram import Update, ReplyKeyboardMarkup, Message
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext, CallbackQueryHandler, PollAnswerHandler,
)

POLL_STATE = 'POLL_STATE'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    utils.main_reply(update.message.reply_text, context)
    return State.FIRST_NODE


def show_change_lang_prompt(reply, context):
    reply_keyboard = [[['Русский', 'ru'], ['Newru', 'newru']]]
    reply('Выберите язык',
          reply_markup=utils.make_inline_keyboard(reply_keyboard))


def first_node(update: Update, context: CallbackContext):
    text = update.message.text
    if text == _(tr.REVIEW, context):
        reply_keyboard = [[_(tr.REVIEW_READ, context), _(tr.REVIEW_ADD, context)], ['Назад']]
        update.message.reply_text('Вы хотите прочитать или добавить?', )
        update.message.reply_text(update.message.text,
                                  reply_markup=ReplyKeyboardMarkup(
                                      reply_keyboard, one_time_keyboard=True
                                  ))
        return State.REVIEW
    elif text == _(tr.HELP_WITH_LEARNING, context):
        return learning_help.start(update, context)
    elif text == _(tr.CHANGE_LANG, context):
        show_change_lang_prompt(update.effective_user.send_message, context)
        return State.CHANGE_LANG
    elif text == _(tr.SEND_FEEDBACK, context):
        return feedback.start(update, context)
    elif len(text) > 0 and text[-1] == '?':
        update.message.reply_text(_(tr.PASTA_STUDOFIS, context))


def choose_lang(update, context):
    data, reply = utils.answer_query(update, context)
    context.user_data['lang'] = data
    reply('Успешно!')
    utils.main_reply(update.effective_user.send_message, context)
    return State.FIRST_NODE


def main():
    from config import token
    updater = Updater(token, use_context=True)

    dispatcher = updater.dispatcher

    main_conv = ConversationHandler(
        entry_points=[MessageHandler(Filters.text, start)],
        states={
            State.FIRST_NODE: [MessageHandler(Filters.text, first_node)],
            State.CHANGE_LANG: [CallbackQueryHandler(choose_lang)],
            **learning_help.get_states(),
            **teachers_review.get_states(),
            **feedback.get_states()
        },
        fallbacks=[]
    )

    dispatcher.add_handler(main_conv)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
