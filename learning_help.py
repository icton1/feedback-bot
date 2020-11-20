from telegram import (
    Update, CallbackQuery, User
)
from telegram.ext import CallbackQueryHandler

from translations import gettext as _
import translations as tr
from keyboard_utils import make_inline_keyboard, get_main_keyboard

from constants import State, CallbackQueryAnswer as Answer


def start(update: Update, context):
    reply_keyboard = make_inline_keyboard(
        [[[_(tr.POPULAR_SUBJECT1, context), Answer.HELP_POP_SUBJ1],
          [_(tr.POPULAR_SUBJECT2, context), Answer.HELP_POP_SUBJ2]],
         [[_(tr.POPULAR_SUBJECT3, context), Answer.HELP_POP_SUBJ3],
          [_(tr.POPULAR_SUBJECT_OTHER, context), Answer.HELP_POP_SUBJ_OTHER]]]
    )
    update.message.reply_text(_(tr.CHOOSE_YOUR_SUBJECT, context),
                              reply_markup=reply_keyboard)
    return State.HELP_INLINE_CHOOSING


def chose_subject(update: Update, context):
    query: CallbackQuery = update.callback_query
    data = query.data
    query.answer()
    query.edit_message_text(text=f"you pressed {data}")
    update.effective_user.send_message(text="Спасибо!",
                                       reply_markup=get_main_keyboard(context))
    return State.FIRST_NODE


def get_states():
    return {
        State.HELP_INLINE_CHOOSING: [CallbackQueryHandler(chose_subject)],
    }
