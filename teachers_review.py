from telegram import (
    Update, CallbackQuery
)
from telegram.ext import CallbackQueryHandler, MessageHandler, Filters, CallbackContext

from translations import gettext as _
import translations as tr
from keyboard_utils import make_inline_keyboard, get_main_keyboard
import bd_worker


from states import State
def start(update: Update, context: CallbackContext):
    if update.message.text=='Добавить':
        return State.ADD_T
    elif update.message.text=='Читать':
        return State.READ_T
    return None

def add_t(update: Update, context: CallbackContext):
    pass

def read_t(update: Update, context: CallbackContext):
    update.message.reply_text(bd_worker.find_teacher(update.message.text)[0])

def get_states():
    return {
        State.REVIEW: [MessageHandler(Filters.text, start)],
        State.ADD_T: [MessageHandler(Filters.text, add_t)],
        State.READ_T: [MessageHandler(Filters.text, read_t)]
    }