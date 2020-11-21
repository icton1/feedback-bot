from telegram import (
    Update, CallbackQuery
)
from telegram.ext import CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import translations
import bd_worker
import translations as tr
from translations import gettext as _

from states import State
def start(update: Update, context: CallbackContext):
    if update.message.text==_(tr.REVIEW_ADD, 'ru'):
        return State.ADD_T
    elif update.message.text==_(tr.REVIEW_READ, 'ru'):
        return State.READ_T
    return None

def add_t(update: Update, context: CallbackContext):
    update.message.reply_text("Введите ФИО преподователя")


def read_t(update: Update, context: CallbackContext):
    update.message.reply_text("Начните вводить имя преподователя")
    update.message.reply_text(bd_worker.find_teacher(update.message.text))

def get_name(update: Update, context: CallbackContext):
    pass

def get_states():
    return {
        State.REVIEW: [MessageHandler(Filters.text, start)],
        State.ADD_T: [MessageHandler(Filters.text, add_t)],
        State.READ_T: [MessageHandler(Filters.text, read_t)]
    }