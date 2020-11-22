from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackQueryHandler, MessageHandler, CallbackContext
import bd_worker as bd_worker  # wont work without this line (joke)
import translations as tr
from translations import gettext as _
from utils import (
    main_reply, MESSAGE_FILTER, save_list_keyboard,
    show_list_keyboard, handle_list_keyboard_query, save_subject_keyboards,
    show_subjects, save_teachers_read_keyboards, save_teachers_add_keyboards, ANSWER_NOT_IN_LIST, show_teachers,
    ANSWER_TYPE_AGAIN
)

from states import State


def start(update: Update, context: CallbackContext):
    reply_keyboard = [[_(tr.REVIEW_READ, context),
                       _(tr.REVIEW_ADD, context)],
                      [_(tr.BACK, context)]]
    update.message.reply_text(_(tr.READ_OR_ADD, context),
                              reply_markup=ReplyKeyboardMarkup(
                                  reply_keyboard, one_time_keyboard=True
                              ))
    return State.REVIEW


def choose_action_type(update: Update, context: CallbackContext):
    # TODO back button
    reply_keyboard = [[_(tr.BACK, context)]]
    if update.message.text == _(tr.REVIEW_ADD, context):
        save_subject_keyboards(bd_worker.get_all_subjects(), context)
        show_subjects(update.message.reply_text, context)
        return State.ADD_TO_SUBJECT
    elif update.message.text == _(tr.REVIEW_READ, context):
        save_subject_keyboards(bd_worker.get_all_subjects(), context)
        show_subjects(update.message.reply_text, context)
        return State.READ_FROM_SUBJECT
    elif update.message.text == _(tr.BACK, context):
        main_reply(update.message.reply_text, context)
        return State.FIRST_NODE
    return None


def read_from_subject(update: Update, context: CallbackContext):
    def choose_option(update, context, data, reply):
        if data == _(tr.BACK, context):
            main_reply(reply, context)
            return State.FIRST_NODE
        context.user_data['subject'] = data
        reply(_(tr.START_INPUTING_NAMES, context))
        return State.READ_T

    return handle_list_keyboard_query(update, context,
                                      show_subjects, choose_option)


def add_to_subject(update: Update, context: CallbackContext):
    def choose_option(update, context, data, reply):
        if data == _(tr.BACK, context):
            main_reply(reply, context)
            return State.FIRST_NODE
        elif data == ANSWER_NOT_IN_LIST:
            reply("Введите название предмета")
            return State.ADD_NEW_SUBJECT
        context.user_data['subject'] = data
        reply(_(tr.INPUT_FIO, context))
        return State.ADD_T

    return handle_list_keyboard_query(update, context,
                                      show_subjects, choose_option)


def add_new_subject(update: Update, context: CallbackContext):
    bd_worker.add_new_subject(update.message.text)
    context.user_data['subject'] = update.message.text
    update.message.reply_text("Предмет успешно добавлен")
    update.message.reply_text(_(tr.INPUT_FIO, context))
    return State.ADD_T

def add_t(update: Update, context: CallbackContext):
    teachers = bd_worker.find_teachers(context.user_data['subject'],
                                       update.message.text)
    if teachers:
        context.user_data['teacher_name'] = update.message.text
        save_teachers_add_keyboards(teachers, context)
        show_teachers(update.message.reply_text, context)
        return State.ADD_T_INLINE
    else:
        context.user_data['teacher_name'] = update.message.text
        update.message.reply_text(_(tr.OTZYV, context))
        return State.ADD_DESC


def addictional_add(update, context):
    context.user_data['teacher_name'] = update.message.text
    update.message.reply_text(_(tr.OTZYV, context))
    return State.ADD_DESC


def add_t_inline(update, context):
    def choose_option(update, context, data, reply):
        if data == ANSWER_NOT_IN_LIST:
            reply(_(tr.INPUT_ALL_FIO, context))
            return State.ADDICTIONAL_ADD
        else:
            context.user_data['teacher_name'] = data
            reply(_(tr.OTZYV, context))
            return State.ADD_DESC

    return handle_list_keyboard_query(update, context,
                                      show_teachers, choose_option)


def show_teacher_feedback(reply, teacher_name, context):
    teacher = bd_worker.read_teacher(context.user_data['subject'], teacher_name)
    rating = str(sum(teacher["ratings"]) / len(teacher["ratings"]))
    reviews = _(tr.REVIEWS_SEPARATOR, context).join(teacher["feedback"])
    msg = _(tr.TEACHER_FEEDBACK_PATTERN, context).format(
        teacher=teacher_name, rating=rating, reviews=reviews
    )
    reply(msg)


def read_t(update: Update, context: CallbackContext):
    teachers = bd_worker.find_teachers(context.user_data['subject'],
                                       update.message.text)
    if len(teachers) == 0:
        update.message.reply_text(_(tr.TEACHER_NOT_FOUND, context))
    elif len(teachers) > 1:
        save_teachers_read_keyboards(teachers, context)
        show_teachers(update.message.reply_text, context)
        return State.READ_T_INLINE
    else:
        show_teacher_feedback(update.message.reply_text, teachers[0], context)
        main_reply(update.message.reply_text, context)
        return State.FIRST_NODE


def read_t_inline(update, context):
    def choose_option(update, context, data, reply):
        if data == ANSWER_TYPE_AGAIN:
            reply(_(tr.START_INPUTING_NAMES, context))
            return State.READ_T
        else:
            show_teacher_feedback(reply, data, context)
            main_reply(update.effective_user.send_message, context)
            return State.FIRST_NODE

    return handle_list_keyboard_query(update, context,
                                      show_teachers, choose_option)


def add_desc(update: Update, context: CallbackContext):
    context.user_data['teacher_desc'] = update.message.text
    update.message.reply_text(_(tr.HOW_REVIEW_TEACHER, context))
    return State.ADD_RATING


def add_rating(update: Update, context: CallbackContext):
    if update.message.text.isnumeric() and 0 <= int(update.message.text) <= 10:
        context.user_data['teacher_rating'] = update.message.text
        teacher = bd_worker.read_teacher(context.user_data['subject'],
                                         context.user_data['teacher_name'])
        if not teacher:
            bd_worker.add_new_teacher(context.user_data['subject'],
                                      context.user_data['teacher_name'],
                                      context.user_data['teacher_desc'],
                                      context.user_data['teacher_rating'])
        else:
            bd_worker.add_new_description(context.user_data['subject'],
                                          context.user_data['teacher_name'],
                                          context.user_data['teacher_desc'],
                                          context.user_data['teacher_rating'])
        update.message.reply_text(_(tr.EXCELLENT, context))
        main_reply(update.message.reply_text, context)
        return State.FIRST_NODE
    else:
        update.message.reply_text(
            _(tr.WRONG_RATING, context))
        return None


def get_states():
    return {
        State.REVIEW: [MessageHandler(MESSAGE_FILTER, choose_action_type)],
        State.ADDICTIONAL_ADD: [MessageHandler(MESSAGE_FILTER,
                                               addictional_add)],
        State.ADD_T: [MessageHandler(MESSAGE_FILTER, add_t)],
        State.READ_T: [MessageHandler(MESSAGE_FILTER, read_t)],
        State.READ_T_INLINE: [CallbackQueryHandler(read_t_inline)],
        State.ADD_T_INLINE: [CallbackQueryHandler(add_t_inline)],
        State.ADD_DESC: [MessageHandler(MESSAGE_FILTER, add_desc)],
        State.ADD_RATING: [MessageHandler(MESSAGE_FILTER, add_rating)],
        State.READ_FROM_SUBJECT: [CallbackQueryHandler(read_from_subject)],
        State.ADD_TO_SUBJECT: [CallbackQueryHandler(add_to_subject)],
        State.ADD_NEW_SUBJECT: [MessageHandler(MESSAGE_FILTER, add_new_subject)],
    }
