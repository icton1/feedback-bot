from telegram import (
    Update, CallbackQuery, ReplyKeyboardMarkup
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
    elif update.message.text == _(tr.REVIEW_READ, context):
        update.message.reply_text("Начните вводить имя преподователя")
        return State.READ_T
    return None


def add_t(update: Update, context: CallbackContext):
    context.user_data['teacher_name'] = update.message.text
    update.message.reply_text("Оставьте отзыв о преподователе")
    return State.ADD_DESC


def read_t(update: Update, context: CallbackContext):
    if True:#try:
        teachers = bd_worker.find_teacher(update.message.text)
        if len(teachers) == 0:
            update.message.reply_text('Такого преподователя не найдено')
        elif len(teachers) > 1:
            # TODO переделать на inline кнопки
            update.message.reply_text('Найдено {} преподователей. Кто вас интересует?'.format(len(teachers)))
            update.message.reply_text('\n'.join(teachers))
        else:
            teacher = bd_worker.read_teacher(bd_worker.find_teacher(teachers[0])[0])
            msg = str(bd_worker.find_teacher(teachers[0])[0]) + '\nОтзывы: ' + '\n***\n'.join(teacher["feedback"]) + '\nРейтинг: ' + str(sum(teacher["ratings"])/len(teacher["ratings"]))
            print(msg)
            update.message.reply_text(msg)
    else:#except Exception as e:
        #print(e)
        update.message.reply_text('Такого преподователя не найдено')


def add_desc(update: Update, context: CallbackContext):
    context.user_data['teacher_desc'] = update.message.text
    update.message.reply_text("Как вы оцените преподователя? (из 10)")
    return State.ADD_RATING


def add_rating(update: Update, context: CallbackContext):
    if update.message.text.isnumeric() and 0 <= int(update.message.text) <= 10:
        context.user_data['teacher_rating'] = update.message.text
        bd_worker.add_new_teacher(context.user_data['teacher_name'], context.user_data['teacher_desc'],
                                  context.user_data['teacher_rating'])
        reply_keyboard = [[_(tr.HELLO, context)],
                          ['Обратиться в центр качества образования',
                           'Нужна помощь с предметом?'],
                          [_(tr.REVIEW, context)]]
        update.message.reply_text(update.message.text,
                                  reply_markup=ReplyKeyboardMarkup(
                                      reply_keyboard, one_time_keyboard=True
                                  ))
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
