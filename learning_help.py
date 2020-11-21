from telegram import (
    Update, CallbackQuery
)
from telegram.ext import CallbackQueryHandler, MessageHandler, Filters

from translations import gettext as _
import translations as tr
from keyboard_utils import make_inline_keyboard, get_main_keyboard

from states import State

SUBJECT = 'subject'
HELP_TYPE = 'help type'
AWARD = 'award'
DESCRIPTION = 'description'


class Answer:
    POP_SUBJ_OTHER = 'HELP_POP_SUBJ_OTHER'
    TYPE_TOGETHER = 'TYPE_TOGETHER'
    IM_WEAK = 'IM_WEAK'
    IM_STRONK = 'IM_STRONK'

    SUBJECT_AGAIN = 'SUBJECT_AGAIN'
    TYPE_AGAIN = 'TYPE_AGAIN'
    AWARD_AGAIN = 'AWARD_AGAIN'
    DESCRIPTION_AGAIN = 'DESCRIPTION_AGAIN'
    NO_INPUT_AGAIN = 'NO_INPUT_AGAIN'


''' PROMPTS '''


def choose_subject_prompt(reply, context):
    reply_keyboard = make_inline_keyboard(
        [[[_(tr.POPULAR_SUBJECT1, context)] * 2,
          [_(tr.POPULAR_SUBJECT2, context)] * 2],
         [[_(tr.POPULAR_SUBJECT3, context)] * 2,
          [_(tr.POPULAR_SUBJECT_OTHER, context), Answer.POP_SUBJ_OTHER]]]
    )
    reply(_(tr.CHOOSE_YOUR_SUBJECT, context), reply_markup=reply_keyboard)


def choose_other_type_prompt(reply, context):
    reply(_(tr.POPULAR_SUBJECT_OTHER_PROMPT, context))


def choose_type_prompt(reply, context):
    reply_keyboard = make_inline_keyboard(
        [[[_(tr.HELP_TYPE_TOGETHER, context), Answer.TYPE_TOGETHER]],
         [[_(tr.HELP_TYPE_IM_WEAK, context), Answer.IM_WEAK],
          [_(tr.HELP_TYPE_IM_STRONK, context), Answer.IM_STRONK]]]
    )
    reply(
        text=_(tr.CHOOSE_HELP_TYPE, context),
        reply_markup=reply_keyboard
    )


def choose_award_prompt(reply, context):
    reply(_(tr.HELP_AWARD_PROMPT, context))


def choose_description_prompt(reply, context):
    reply(_(tr.HELP_DESCRIPTION_PROMPT, context))


def check_request_prompt(reply, context):
    reply_keyboard = make_inline_keyboard(
        [[[_(tr.HELP_TYPE_TOGETHER, context), Answer.TYPE_TOGETHER]],
         [[_(tr.HELP_TYPE_IM_WEAK, context), Answer.IM_WEAK],
          [_(tr.HELP_TYPE_IM_STRONK, context), Answer.IM_STRONK]]]
    )
    reply(
        text=_(tr.CHOOSE_HELP_TYPE, context),
        reply_markup=reply_keyboard
    )

    reply("Проверь заявку (TODO)")


def wait_for_matching_prompt(reply, context):
    reply("Мэтчинг... (TODO)")


''' NODES '''


def answer_query(update, context):
    query: CallbackQuery = update.callback_query
    data = query.data
    query.answer()
    return data, query.edit_message_text


def start(update: Update, context):
    choose_subject_prompt(update.message.reply_text, context)
    return State.HELP_CHOSE_SUBJECT


def chose_subject(update: Update, context):
    data, reply = answer_query(update, context)
    if data == Answer.POP_SUBJ_OTHER:
        choose_other_type_prompt(reply, context)
        return State.HELP_CHOSE_SUBJECT_OTHER

    context.user_data[SUBJECT] = data
    choose_type_prompt(reply, context)
    return State.HELP_CHOSE_TYPE


def chose_other_subject(update, context):
    context.user_data[SUBJECT] = update.message.text
    choose_type_prompt(update.effective_user.send_message, context)
    return State.HELP_CHOSE_TYPE


def chose_type(update, context):
    data, reply = answer_query(update, context)
    context.user_data[HELP_TYPE] = data

    if data == Answer.TYPE_TOGETHER or data == Answer.IM_STRONK:
        choose_description_prompt(reply, context)
        return State.HELP_MATCHING
    elif data == Answer.IM_WEAK:
        choose_award_prompt(reply, context)
        return State.HELP_CHOSE_AWARD

    raise ValueError('Bad value from inline answer')


def chose_award(update, context):
    context.user_data[AWARD] = update.message.text
    choose_description_prompt(update.effective_user.send_message, context)
    return State.HELP_CHOSE_DESCRIPTION


def chose_description(update, context):
    context.user_data[DESCRIPTION] = update.message.text
    check_request_prompt(update.effective_user.send_message, context)
    return State.HELP_CHECKING_REQUEST


def check_request(update, context):
    data, reply = answer_query(update, context)

    if data == Answer.SUBJECT_AGAIN:
        choose_subject_prompt(reply, context)
        return State.HELP_SUBJECT_AGAIN
    elif data == Answer.TYPE_AGAIN:
        choose_type_prompt(reply, context)
        return State.HELP_TYPE_AGAIN
    elif data == Answer.AWARD_AGAIN:
        choose_award_prompt(reply, context)
        return State.HELP_AWARD_AGAIN
    elif data == Answer.DESCRIPTION_AGAIN:
        choose_description_prompt(reply, context)
        return State.HELP_DESCRIPTION_AGAIN
    elif data == Answer.NO_INPUT_AGAIN:
        wait_for_matching_prompt(reply, context)
        return State.HELP_MATCHING

    raise ValueError('Bad value from inline answer')


def on_exit(update, context):
    update.effective_user.send_message(_(tr.HELP_LAST_PHRASE, context),
                                       reply_markup=get_main_keyboard(context))
    return State.FIRST_NODE


def get_states():
    return {
        State.HELP_CHOSE_SUBJECT: [CallbackQueryHandler(chose_subject)],
        State.HELP_CHOSE_SUBJECT_OTHER: [
            MessageHandler(Filters.text, chose_other_subject)
        ],
        State.HELP_CHOSE_TYPE: [CallbackQueryHandler(chose_type)],
        State.HELP_CHOSE_AWARD: [
            MessageHandler(Filters.text, chose_description)
        ],
        State.HELP_CHOSE_DESCRIPTION: [
            MessageHandler(Filters.text, chose_award)
        ],
        State.HELP_CHECKING_REQUEST: [
            MessageHandler(Filters.text, check_request)
        ],
        # State.HELP_SUBJECT_AGAIN: [
        #     MessageHandler(Filters.text, chose_subject_again)
        # ],
        # State.HELP_SUBJECT_OTHER_AGAIN: [
        #     MessageHandler(Filters.text, chose_subject_other_again)
        # ],
        # State.HELP_TYPE_AGAIN: [
        #     MessageHandler(Filters.text, chose_type_again)
        # ],
        # State.HELP_AWARD_AGAIN: [
        #     MessageHandler(Filters.text, chose_award_again)
        # ],
        # State.HELP_DESCRIPTION_AGAIN: [
        #     MessageHandler(Filters.text, chose_description_again)
        # ],
        # State.HELP_MATCHING: [
        #     MessageHandler(Filters.text, match)
        # ],
    }
