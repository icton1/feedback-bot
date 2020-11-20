HELLO = {'ru': 'Привет', 'newru': "ПрИвЕт!"}
HELP_WITH_LEARNING = {'ru': 'Нужна помощь с предметом?'}
CHOOSE_YOUR_SUBJECT = {'ru': 'Выберите предмет'}
POPULAR_SUBJECT1 = {'ru': 'Креатех'}
POPULAR_SUBJECT2 = {'ru': 'КИК'}
POPULAR_SUBJECT3 = {'ru': 'Физра'}
POPULAR_SUBJECT_OTHER = {'ru': 'Сам введу'}


def gettext(phrase, context):
    lang = context.user_data.get('lang', 'ru')
    return phrase[lang] if lang in phrase.keys() else phrase['ru']
