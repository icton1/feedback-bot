# Доступные языки
LANGUAGES = [
   # Каждый массив -- строка в менюшке выбора языка
   [
       # Каждый массив -- пара строк:
       # ['Название в менюшке', 'Название в этом файле']
       ['Русский', 'ru'],
       ['Новый русский', 'newru']
   ]
]
SELECT_LANG = {'ru': 'Выберите язык', 'newru': "Селект лангуаге"
}
SUCCESSFULLY_SELECTED_LANG = {'ru': 'Успешно!', 'newru': "Чудненько!"} # с кайфом!


# Кнопочки в главном меню
MENU_HELLO = {'ru': 'Привет', 'newru': "Здарова"}
MENU_REVIEW = {'ru': 'Отзыв о преподователе', 'newru': "Перемыть косточки"}
MENU_SELECT_LANG = {'ru': 'Поменять язык', 'newru': "Сменить лангуаге"}
MENU_SEND_FEEDBACK = {'ru': 'Оставить обратную связь', 'newru': "Пошушукаемся"}


HELLO_TEXT = {'ru': '''
Ну, привет)
Я пришел в этот мир, чтобы сделать обратную связь удобнее и забавнее. Скажем нет ругательствам, глупым вопросам и скучным опросам.
Хочешь разнообразия? Смени язык на "новый русский".
Хочешь сладких апельсинов? Сходи в магазин.
Напиши /stop если чувствуешь нужду выйти в главное меню.
''',
'newru': '''
Маме привет, остальным соболезную!/Мир вашему дому!
Меня создали для получения удовольствия и перенаправления в студофис по всем вопросам.
Я хочу чтобы ты потрогал меня везде... Перемой косточки всем преподавателям, пройди все опросы по дисциплинам, чтобы улучшить качество твоего образования.
/stop - самое неклассическое стоп-слово для перехода в главное меню. Только помни, что пожарные машины на красный свет не останавливаются😉
'''}
GOT_TO_MAIN_MENU = {'ru': 'Вы перешли в главное меню', 'newru': "Не смотри. Действуй!"}


# Это видимо одна фраза для всех кнопок вида "Назад", но это не точно
BACK = {'ru': 'Назад', 'newru': "Отставить"}


# Листаем по страничкам (например, выбираем препода)
LAST_PAGE = {'ru': '<<< Назад', 'newru': "Cто шагов назад"}#Вернуться в семью
NEXT_PAGE = {'ru': '>>> Далее', 'newru': "Только вперёд!"}#у самурая нет цели, только путь...


# Дальше идут фразы из фичи Семена
READ_OR_ADD = {'ru': 'Вы хотите прочитать или добавить?', 'newru': "Пришел чекнуть тред или рассказать сенсацию?"}
REVIEW_READ = {'ru': 'Читать', 'newru': "Последние сводки"}
REVIEW_ADD = {'ru': 'Добавить', 'newru': "Подержать в курсе"}


#INPUT_SUBJ_NAME = {'ru': 'Введите название предмета', 'newru': "Вопрос на четверочку: Че за предмет у тебя?"}
INPUT_FIO = {'ru': 'Введите ФИО преподавателя', 'newru': "Вопрос на пятерку: Как зовут преподавателя? "}
OTZYV = {'ru': 'Оставьте отзыв о преподавателе', 'newru': "Ну и как он/она в плане учёбы?"}
INPUT_ALL_FIO = {'ru': 'Введите полное ФИО', 'newru': "Напиши ФИО с уважением!"}
WRITE_ONE_MORE = {'ru': 'Написать заново', 'newru': "Перепуточки"}
START_INPUTING_NAMES = {'ru': 'Начните вводить имя преподавателя', 'newru': "Никнейм преподавателя по паспорту"}
TEACHER_LIST_TITLE = {'ru': 'Преподаватели', 'newru': "Преподы"}
SUBJECT_LIST_TITLE = {'ru': 'Выберите предмет'}
TEACHER_NOT_FOUND = {'ru': 'Такого преподавателя не найдено', 'newru': "А нету такого! Возможно, это твой воображаемый друг..."}
HOW_REVIEW_TEACHER = {'ru': "Как вы оцените преподавателя? (из 10)", 'newru': "На сколько он крут по десятибалльной?"}#надо поменять
EXCELLENT = {'ru': 'Ответ успешно добавлен', 'newru': 'Ваш ответ никому не нужен, но все о нём теперь знают. Ой, то есть "Ваш ответ успешно добавлен" '}
WRONG_RATING = {'ru': 'Неправильный рейтинг, выберите число от 0 до 10', 'newru': "Русским по белому написано от 0 до 10. Приём, как слышно? Повторяю: от 0 до 10."}

# При выборе учителя / предмета в списке
NOT_IN_LIST = {'ru': 'Нет в списке', 'newru': "Ох, никого не нашлось"}

# Тут как мы показываем отзыв
TEACHER_FEEDBACK_PATTERN = {'ru': '''
{teacher}
Рейтинг: {rating}
Отзывы:
{reviews}
''',
'newru':  '''
{teacher}
Садись, {rating}
Что говорят крысы за спиной у кисы:
{reviews}
'''}

REVIEWS_SEPARATOR = {'ru': '\n🤪🤪🤪🤪🤪🤪\n', 'newru':  '\n🤪🤪🤪🤪🤪🤪\n'}


# Дальше идут фразы из фичи Миши
STRING_POLLS = {
   'ru': [
       ['На данный момент как вы оцениваете предмет?', ['Позитивно', 'Нейтрально', 'Негативно']],
       ['Как вы оцениваете количество пар по данному предмету?', ['Меня устраивает количество', 'Хотелось бы меньше', 'Хотелось бы больше', 'Считаю, что предмет не нужен и следует его убрать', 'Затрудняюсь ответить']],
       ['Какой формат работы на данном предмете вам кажется оптимальным?', ['Работа в команде', 'Индивидуально', 'Не имеет значения']],
       ['Устраивает ли вас то, как преподаватель проводит дисциплину?', ['Да, всё отлично', 'Можно лучше', 'Приемлемо', 'Не устраивает', 'ответов1', 'ответов1']],
       [' Оставлять ли этот предмет в учебном плане? ', ['Да, он полезный', ' Нет ', 'Затрудняюсь ответить']],
   ],
   'newru': [
       ['Ну и как тебе предмет, сладкий?', ['Апупенный', 'Четвертинка наполовинку', 'Фуфло']],
       ['Что можешь сказать по количеству пар?', ['Тютелька в тютельку', '', 'Слишком много, в меня столько не влезает', 'Ой, а разговоров-то было!', 'Пофек']],
       ['Идеальный формат работы', ['Сколотить дринк тим/попасть в суйсайд сквад', 'Всолянчик', 'До звезды']],
       ['Как тебе препод?', ['Лучший человек в мире', 'Я бы дал ему пару консультаций', 'Норм', '', 'Я проведу в сто раз лучше']],# заменяем Путiна на что-то
       ['Нужный предмет?', ['Всё полезно, что в учебный план полезло ', 'Только чтобы прогуливать', 'Не теряю надежды, что смогу применить оттуда хоть что-то']],
   ],
}
YES = {'ru': 'Да', 'newru': "Угу"}
NO = {'ru': 'Нет', 'newru': "Не угу"}
FEEDBACK_FINAL_PHRASE = {'ru': 'Спасибо за ваш ответ!', 'newru': "От души спасибо папаша"}
WANT_ENTER_POLL_COMMENT = {'ru': 'Хотите добавить комментарий?', 'newru': "Тебе есть что сказать?"}
PLEASE_ENTER_POLL_COMMENT = {'ru': 'Что бы вы посоветовали для улучшения проведения данной дисциплины?', 'newru': "Давай, нападай"}



# Уточни этот вопрос у Студенческого офиса Университета ИТМО
PASTA_STUDOFIS = {'ru': '''
Уточни этот вопрос у Студенческого офиса Университета ИТМО
Они работают с 9 до 19 каждый будний день и будут рады ответить тебе по телефону или по почте
Пожалуйста, грамотно составь письмо или будь вежлив при телефонном звонке
А ещё можно попробовать найти информацию самостоятельно на сайте
Впредь прошу понять, что этот бот не является компетентными в решении похожих вопросов. Именно поэтому, для решения таких проблем была создана "единая точка входа" - Студенческий офис.
'''}

# Легаси. Не трогать.
HELP_WITH_LEARNING = {'ru': 'Легаси. Не трогать.'}
CHOOSE_YOUR_SUBJECT = {'ru': 'Легаси. Не трогать.'}
POPULAR_SUBJECT1 = {'ru': 'Легаси. Не трогать.'}
POPULAR_SUBJECT2 = {'ru': 'Легаси. Не трогать.'}
POPULAR_SUBJECT3 = {'ru': 'Легаси. Не трогать.'}
POPULAR_SUBJECT_OTHER = {'ru': 'Легаси. Не трогать.'}
POPULAR_SUBJECT_OTHER_PROMPT = {'ru': 'Легаси. Не трогать.'}
CHOOSE_HELP_TYPE = {'ru': 'Легаси. Не трогать.'}
HELP_TYPE_TOGETHER = {'ru': 'Легаси. Не трогать.'}
HELP_TYPE_IM_WEAK = {'ru': 'Легаси. Не трогать.'}
HELP_TYPE_IM_STRONK = {'ru': 'Легаси. Не трогать.'}
HELP_AWARD_PROMPT = {'ru': 'Легаси. Не трогать.'}
HELP_DESCRIPTION_PROMPT = {'ru': 'Легаси. Не трогать.'}
HELP_LAST_PHRASE = {'ru': 'Легаси. Не трогать.'}
HELP_CHECK_REQUEST = {'ru': 'Легаси. Не трогать.'}
HELP_SUBJECT = {'ru': 'Легаси. Не трогать.'}
HELP_TYPE = {'ru': 'Легаси. Не трогать.'}
HELP_AWARD = {'ru': 'Легаси. Не трогать.'}
HELP_DESCRIPTION = {'ru': 'Легаси. Не трогать.'}
HELP_CHECK_OK = {'ru': 'Легаси. Не трогать.'}


def gettext(phrase, context):
    lang = context.user_data.get('lang', 'ru')
    return phrase[lang] if lang in phrase.keys() else phrase['ru']
