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
    if update.message.text == _(tr.REVIEW_ADD, context):
        update.message.reply_text("Введите ФИО преподователя")
        return State.ADD_T
    elif update.message.text==_(tr.REVIEW_READ, context):
        return State.READ_T
    return None

def add_t(update: Update, context: CallbackContext):
    context.user_data['teacher_name'] = update.message.text
    update.message.reply_text("Оставьте отзыв о преподователе")
    return State.ADD_DESC

def read_t(update: Update, context: CallbackContext):
    update.message.reply_text("Начните вводить имя преподователя")
    try:
        update.message.reply_text(bd_worker.find_teacher(update.message.text[0]))
    except:
        update.message.reply_text(bd_worker.find_teacher('Такого преподователя не найдено'))

def add_desc(update: Update, context: CallbackContext):
    context.user_data['teacher_desc'] = update.message.text
    update.message.reply_text("Как вы оцените преподователя? (из 10)")
    return State.ADD_RATING

def add_rating(update: Update, context: CallbackContext):
    if update.message.text.isalnum() and 0<=int(update.message.text)<=10:
        context.user_data['teacher_rating'] = update.message.text
        bd_worker.add_new_teacher(context.user_data['teacher_name'], context.user_data['teacher_desc'], context.user_data['teacher_rating'])
        return State.FIRST_NODE
    else:
        update.message.reply_text('Неправильный рейтинг, выберите число от 0 до 10')
        return None

def get_states():
    return {
        State.REVIEW: [MessageHandler(Filters.text, start)],
        State.ADD_T: [MessageHandler(Filters.text, add_t)],
        State.READ_T: [MessageHandler(Filters.text, read_t)],
        State.ADD_DESC: [MessageHandler(Filters.text, add_desc)],
        State.ADD_RATING: [MessageHandler(Filters.text, add_rating)],
    }