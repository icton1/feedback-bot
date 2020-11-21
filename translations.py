HELLO = {'ru': 'Привет', 'newru': "ПрИвЕт!"}
REVIEW = {'ru': 'Отзыв о преподователе', 'newru': "ОтзЫВ о ПрепоДОвАтелЕ"}
CHANGE_LANG = {'ru': 'Поменять язык'}

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
HELP_CHECK_REQUEST = {'ru': 'Проверь данные. Что хочешь поменять?'}
HELP_SUBJECT = {'ru': 'Предмет'}
HELP_TYPE = {'ru': 'Способ помощи'}
HELP_AWARD = {'ru': 'Награда'}
HELP_DESCRIPTION = {'ru': 'Описание'}
HELP_CHECK_OK = {'ru': 'Все ок!'}
SELECT_LANG = {'ru': 'Выберите язык'}
REVIEW_ADD = {'ru': 'Добавить'}
REVIEW_READ = {'ru': 'Читать'}
BACK = {'ru':'Назад'}
READ_OR_ADD = {'ru':'Вы хотите прочитать или добавить?'}
INPUT_SUBJ_NAME = {'ru':'Введите название предмета'}
INPUT_FIO = {'ru':'Введите ФИО преподователя'}
OTZYV = {'ru':'Оставьте отзыв о преподователе'}
INPUT_ALL_FIO = {'ru':'Введите полное ФИО'}
WRITE_ONE_MORE = {'ru':'Написать заново'}

START_INPUTING_NAMES = {'ru':'"Начните вводить имя преподователя"'}

PASTA_STUDOFIS = {'ru': '''
Уточни этот вопрос у Студенческого офиса Университета ИТМО
Они работают с 9 до 19 каждый будний день и будут рады ответить тебе по телефону или по почте
Пожалуйста, грамотно составь письмо или будь вежлив при телефонном звонке
А ещё можно попробовать найти информацию самостоятельно на сайте
Впредь прошу понять, что этот бот не является компетентными в решении похожих вопросов. Именно поэтому, для решения таких проблем была создана "единая точка входа" - Студенческий офис.
'''}


def gettext(phrase, context):
    lang = context.user_data.get('lang', 'ru')
    return phrase[lang] if lang in phrase.keys() else phrase['ru']
