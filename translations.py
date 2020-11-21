HELLO = {'ru': 'Привет', 'newru': "ПрИвЕт!"}
REVIEW = {'ru': 'Отзыв о преподователе', 'newru': "ОтзЫВ о ПрепоДОвАтелЕ"}

HELP_WITH_LEARNING = {'ru': 'Нужна помощь с предметом?'}
CHOOSE_YOUR_SUBJECT = {'ru': 'Выберите предмет'}
POPULAR_SUBJECT1 = {'ru': 'Креатех'}
POPULAR_SUBJECT2 = {'ru': 'КИК'}
POPULAR_SUBJECT3 = {'ru': 'Физра'}
POPULAR_SUBJECT_OTHER = {'ru': 'Сам введу'}
POPULAR_SUBJECT_OTHER_PROMPT = {'ru': 'Ну вводи'}
CHOOSE_HELP_TYPE = {'ru': 'Хто я'}
HELP_TYPE_TOGETHER = {'ru': 'Вместе'}
HELP_TYPE_IM_WEAK = {'ru': 'Он(а) мне'}
HELP_TYPE_IM_STRONK = {'ru': 'Я е(й)му'}
HELP_AWARD_PROMPT = {'ru': 'Скажи сколько готов отдать'}
HELP_DESCRIPTION_PROMPT = {'ru': 'Расскажи о себе, что тебе нужно'}

HELP_LAST_PHRASE = {'ru': 'Пока :('}


def gettext(phrase, context):
    lang = context.user_data.get('lang', 'ru')
    return phrase[lang] if lang in phrase.keys() else phrase['ru']
