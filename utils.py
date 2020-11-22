from telegram import InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardMarkup, CallbackQuery
from telegram.ext import Filters

import translations as tr
from translations import gettext as _


LIST_KEYBOARD = 'LIST_KEYBOARD'
LIST_KEYBOARD_INDEX = 'LIST_KEYBOARD_INDEX'
MAX_INLINE_CHARACTERS = 80
MAX_INLINE_COLUMNS = 1
MAX_INLINE_ROWS = 5

MESSAGE_FILTER = Filters.text & ~Filters.command
ANSWER_FORWARD = 'FORWARD'
ANSWER_BACK = 'BACK'

ANSWER_NOT_IN_LIST = 'NOT_IN_LIST'
ANSWER_TYPE_AGAIN = 'TYPE_AGAIN'


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
            row.append([_(tr.LAST_PAGE, context), ANSWER_BACK])
        if i + MAX_INLINE_ROWS - 1 < len(rows):
            row.append([_(tr.NEXT_PAGE, context), ANSWER_FORWARD])
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

    if data == ANSWER_FORWARD:
        context.user_data[LIST_KEYBOARD_INDEX] += 1
        show(reply, context)
        return None
    elif data == ANSWER_BACK:
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
        lambda: [[_(tr.WRITE_ONE_MORE, context), ANSWER_TYPE_AGAIN]]
    )


def get_add_teachers_keyboards(teachers, context):
    return save_list_keyboard(
        teachers, context,
        lambda: [[_(tr.NOT_IN_LIST, context), ANSWER_NOT_IN_LIST]]
    )


def show_teachers(set_message, context):
    return show_list_keyboard(set_message, context, tr.TEACHER_LIST_TITLE)


def save_subject_keyboards(subjects, context):
    save_list_keyboard(
        subjects, context,
        lambda: [[_(tr.NOT_IN_LIST, context), ANSWER_NOT_IN_LIST]]
    )


def show_subjects(set_message, context):
    return show_list_keyboard(set_message, context, tr.SUBJECT_LIST_TITLE)
