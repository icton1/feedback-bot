import logging
from states import State
import translations as tr
from translations import gettext as _

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    reply_keyboard = [[_(tr.HELLO, context)],
                      ['Обратиться в центр качества образования',
                       'Нужна помощь с предметом?'],
                      ['Отзыв о преподователе']]
    update.message.reply_text(update.message.text,
                              reply_markup=ReplyKeyboardMarkup(
                                  reply_keyboard, one_time_keyboard=True
                              ))
    return State.FIRST_NODE


def read_msg(update: Update, context: CallbackContext):
    print(update.message.text)


def first_node(update: Update, context: CallbackContext):
    if update.message.text == _(tr.HELLO, context):
        reply_keyboard = [['Читать', 'Добавить']]
        update.message.reply_text('Вы хотите прочитать или добавить?', )
        update.message.reply_text(update.message.text,
                                  reply_markup=ReplyKeyboardMarkup(
                                      reply_keyboard, one_time_keyboard=True
                                  ))
        return State.REVIEW


def main():
    from config import token
    updater = Updater(token, use_context=True)

    dispatcher = updater.dispatcher

    main_conv = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            State.FIRST_NODE: [MessageHandler(Filters.text, first_node)],
            State.REVIEW: [MessageHandler(Filters.text, read_msg)]
        },
        fallbacks=[],
    )

    dispatcher.add_handler(main_conv)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
