from telegram import (
    Update, CallbackQuery, ReplyKeyboardMarkup
)
from telegram.ext import CallbackQueryHandler, MessageHandler, Filters, \
    CallbackContext
import bd_worker_new as bd_worker
import translations as tr
from translations import gettext as _
from utils import make_inline_keyboard, main_reply, answer_query

from states import State

LIST_KEYBOARD = 'LIST_KEYBOARD'
LIST_KEYBOARD_INDEX = 'LIST_KEYBOARD_INDEX'
MAX_INLINE_CHARACTERS = 80
MAX_INLINE_COLUMNS = 1
MAX_INLINE_ROWS = 5


class Answers:
    NOT_IN_LIST = 'NOT_IN_LIST'
    TYPE_AGAIN = 'TYPE_AGAIN'
    FORWARD = 'FORWARD'
    BACK = 'BACK'


def save_list_keyboard(options, context,
                       add_additional_buttons=lambda: []):
    rows = [[]]
    last_len = 0
    for option in options:
        if (last_len + len(option) > MAX_INLINE_CHARACTERS
            or len(rows[-1]) + 1 > MAX_INLINE_COLUMNS) \
                and len(rows[-1]) != 0:
            rows.append([])
        rows[-1].append([option] * 2)
    keyboards = []
    for i in range(0, len(rows), MAX_INLINE_ROWS - 1):
        keyboards.append(rows[i:i + MAX_INLINE_ROWS - 1])
        row = [
            *add_additional_buttons()
        ]
        if i > 0:
            row.append([_(tr.LAST_PAGE, context), Answers.BACK])
        if i + MAX_INLINE_ROWS - 1 < len(rows):
            row.append([_(tr.NEXT_PAGE, context), Answers.FORWARD])
        keyboards[-1].append(row)
    context.user_data[LIST_KEYBOARD] = keyboards


def show_list_keyboard(set_message, context, title_phrase):
    keyboard = context.user_data[LIST_KEYBOARD]
    i = context.user_data.setdefault(LIST_KEYBOARD_INDEX, 0)
    keyboard = keyboard[i]
    set_message(text=_(title_phrase, context),
                reply_markup=make_inline_keyboard(keyboard))


def handle_list_keyboard_query(update, context, show, choose_option):
    data, reply = answer_query(update, context)

    if data == Answers.FORWARD:
        context.user_data[LIST_KEYBOARD_INDEX] += 1
        show(reply, context)
        return None
    elif data == Answers.BACK:
        context.user_data[LIST_KEYBOARD_INDEX] -= 1
        show(reply, context)
        return None
    else:
        del context.user_data[LIST_KEYBOARD]
        del context.user_data[LIST_KEYBOARD_INDEX]
        return choose_option(update, context, data, reply)


def save_teachers_keyboards(teachers, context):
    save_list_keyboard(
        teachers, context,
        lambda: [[_(tr.WRITE_ONE_MORE, context), Answers.TYPE_AGAIN]]
    )


def get_add_teachers_keyboards(teachers, context):
    return save_list_keyboard(
        teachers, context,
        lambda: [[_(tr.NOT_IN_LIST, context), Answers.NOT_IN_LIST]]
    )


def show_teachers(set_message, context):
    return show_list_keyboard(set_message, context, tr.TEACHER_LIST_TITLE)


def save_subject_keyboards(subjects, context):
    save_list_keyboard(
        subjects, context,
        lambda: [[_(tr.NOT_IN_LIST, context), Answers.NOT_IN_LIST]]
    )


def show_subjects(set_message, context):
    return show_list_keyboard(set_message, context, tr.SUBJECT_LIST_TITLE)


def start(update: Update, context: CallbackContext):
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
        context.user_data['subject'] = data
        update.message.reply_text(_(tr.INPUT_FIO, context))
        return State.ADD_T

    return handle_list_keyboard_query(update, context,
                                      show_subjects, choose_option)


def add_t(update: Update, context: CallbackContext):
    teachers = bd_worker.find_teachers(context.user_data['subject'], update.message.text)
    if teachers:
        context.user_data['teacher_name'] = update.message.text
        save_teachers_keyboards(teachers, context)
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
        if data == Answers.NOT_IN_LIST:
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
    msg = _(tr.TEACHER_PROFILE_PATTERN, context).format(
        teacher=teacher_name, rating=rating, reviews=reviews
    )
    reply(msg)


def read_t(update: Update, context: CallbackContext):
    teachers = bd_worker.find_teachers(context.user_data['subject'], update.message.text)
    if len(teachers) == 0:
        update.message.reply_text(_(tr.TEACHER_NOT_FOUND, context))
    elif len(teachers) > 1:
        save_teachers_keyboards(teachers, context)
        show_teachers(update.message.reply_text, context)
        return State.READ_T_INLINE
    else:
        show_teacher_feedback(update.message.reply_text, teachers[0], context)
        main_reply(update.message.reply_text, context)
        return State.FIRST_NODE


def read_t_inline(update, context):
    def choose_option(update, context, data, reply):
        if data == Answers.TYPE_AGAIN:
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
        teacher = bd_worker.read_teacher(context.user_data['subject'], context.user_data['teacher_name'])
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
        State.ADDICTIONAL_ADD: [MessageHandler(Filters.text & ~Filters.command, addictional_add)],
        State.REVIEW: [MessageHandler(Filters.text & ~Filters.command, start)],
        State.ADD_T: [MessageHandler(Filters.text & ~Filters.command, add_t)],
        State.READ_T: [MessageHandler(Filters.text & ~Filters.command, read_t)],
        State.READ_T_INLINE: [CallbackQueryHandler(read_t_inline)],
        State.ADD_T_INLINE: [CallbackQueryHandler(add_t_inline)],
        State.ADD_DESC: [MessageHandler(Filters.text & ~Filters.command, add_desc)],
        State.ADD_RATING: [MessageHandler(Filters.text & ~Filters.command, add_rating)],
        State.READ_FROM_SUBJECT: [CallbackQueryHandler(read_from_subject)],
        State.ADD_TO_SUBJECT: [CallbackQueryHandler(add_to_subject)],
    }
