HELLO = {'ru': 'Привет', 'newru': "ПрИвЕт!"}
REVIEW = {'ru': 'Отзыв о преподователе', 'newru': "ОтзЫВ о ПрепоДОвАтелЕ"}

def gettext(phrase, context):
    lang = context.user_data.get('lang', 'ru')
    return phrase[lang] if lang in phrase.keys() else phrase['ru']
