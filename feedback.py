from telegram import Update, PollAnswer
from telegram.ext import PollAnswerHandler, CallbackContext, \
    CallbackQueryHandler, MessageHandler, Filters

import bd_worker
import utils
from states import State
import os
import os.path
import translations as tr
from translations import gettext as _

SUBJECT = 'SUBJECT'
TEACHER = 'TEACHER'
POLL_INDEX = 'POLL_INDEX'
ANSWERS = 'ANSWERS'
ANSWER_COMMENT = 'ANSWER_COMMENT'


class AnonymousPoll:
    def __init__(self, name, answers, many_answers=False):
        self.name = name
        self.answers = answers
        self.many_answers = many_answers

    def send_poll(self, reply):
        keyboard = utils.make_inline_keyboard(
            [[[answer, i]]
             for answer, i in zip(self.answers, range(len(self.answers)))]
        )
        reply(text=self.name, reply_markup=keyboard)

    def get_results_then_next(self, update, context, next_poll):
        data, reply = utils.answer_query(update, context)
        if next_poll is not None:
            next_poll.send_poll(reply)
        return data, reply


POLLS = {
    lang: [AnonymousPoll(*poll) for poll in polls]
    for lang, polls in tr.STRING_POLLS.items()
}


def any_comments_prompt(reply, context):
    reply_keyboard = utils.make_inline_keyboard(
        [[[_(tr.YES, context), 'True'], [_(tr.NO, context), 'False']]]
    )
    reply(text=_(tr.WANT_ENTER_POLL_COMMENT, context),
          reply_markup=reply_keyboard)


def process_polls(update, context):
    lang = context.user_data.get('lang', 'ru')

    poll_index = context.user_data[POLL_INDEX]
    poll = POLLS[lang][poll_index]
    next_poll = POLLS[lang][poll_index + 1] \
        if poll_index + 1 < len(POLLS[lang]) else None

    answer, reply = poll.get_results_then_next(update, context, next_poll)
    context.user_data[ANSWERS].append(answer)

    if next_poll is None:
        del context.user_data[POLL_INDEX]
        any_comments_prompt(reply, context)
        return State.FDBK_POLLS_ASK_COMMENTS
    else:
        context.user_data[POLL_INDEX] = poll_index + 1


def start(update, context):
    utils.save_subject_keyboards(bd_worker.get_all_subjects(), context)
    utils.show_subjects(update.message.reply_text, context)
    return State.FDBK_SUBJECTS_LIST


def save_to_csv(lang, answer):
    os.makedirs('csv', exist_ok=True)
    if not os.path.isfile('csv/table.csv'):
        headers = [f'ans{i}' for i in range(len(POLLS[lang]))] + ['comment']
        with open('csv/table.csv', 'w') as f:
            f.write(','.join(headers))
            f.write(os.linesep)
    with open('csv/table.csv', 'a') as f:
        answer[-1] = '"' + answer[-1].replace('"', "'") + '"'
        f.write(','.join(answer))
        f.write(os.linesep)


def finish(send_first, send_second, context):
    answer = context.user_data[ANSWERS] + [context.user_data[ANSWER_COMMENT]]
    save_to_csv(context.user_data.get('lang', 'ru'), answer)
    send_first(_(tr.FEEDBACK_FINAL_PHRASE, context))
    utils.main_reply(send_second, context)
    return State.FIRST_NODE


def ask_comments(update, context):
    data, reply = utils.answer_query(update, context)
    if data == 'True':
        reply(_(tr.PLEASE_ENTER_POLL_COMMENT, context))
        return State.FDBK_POLLS_GET_COMMENTS
    else:
        context.user_data[ANSWER_COMMENT] = ''
        return finish(reply, update.effective_user.send_message, context)


def get_comments(update, context):
    comment = update.message.text
    context.user_data[ANSWER_COMMENT] = comment
    send_new = update.effective_user.send_message
    return finish(send_new, send_new, context)


def handle_subjects_list(update, context):
    def choose_option(update, context, data, reply):
        context.user_data[SUBJECT] = data
        reply(_(tr.START_INPUTING_NAMES, context))
        return State.FDBK_GET_TEACHER_INFO

    return utils.handle_list_keyboard_query(update, context,
                                            utils.show_subjects, choose_option)


def get_teacher_info(update, context):
    teachers = bd_worker.find_teachers(context.user_data[SUBJECT],
                                       update.message.text)

    utils.save_teachers_keyboards(teachers, context)
    utils.show_teachers(update.message.reply_text, context)
    return State.FDBK_TEACHERS_LIST


def handle_teachers_list(update, context):
    def choose_option(update, context, data, reply):
        if data == utils.ANSWER_TYPE_AGAIN:
            reply(_(tr.START_INPUTING_NAMES, context))
            return State.FDBK_GET_TEACHER_INFO
        else:
            context.user_data[TEACHER] = data
            context.user_data[ANSWERS] = []
            context.user_data[POLL_INDEX] = 0
            poll = POLLS[context.user_data.get('lang', 'ru')][0]
            poll.send_poll(reply)
            return State.FDBK_POLLS

    return utils.handle_list_keyboard_query(update, context,
                                            utils.show_teachers, choose_option)


def get_states():
    return {
        State.FDBK_SUBJECTS_LIST: [CallbackQueryHandler(handle_subjects_list)],
        State.FDBK_GET_TEACHER_INFO: [MessageHandler(utils.MESSAGE_FILTER,
                                                     get_teacher_info)],
        State.FDBK_TEACHERS_LIST: [CallbackQueryHandler(handle_teachers_list)],
        State.FDBK_POLLS: [CallbackQueryHandler(process_polls)],
        State.FDBK_POLLS_ASK_COMMENTS: [CallbackQueryHandler(ask_comments)],
        State.FDBK_POLLS_GET_COMMENTS: [
            MessageHandler(utils.MESSAGE_FILTER, get_comments)
        ],
    }
