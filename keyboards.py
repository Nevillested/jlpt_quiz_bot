from telebot import types

#метод для создания инлайн-клавиатуры. На вход получает словарь из пары "ид кнопки-название кнопки" и количество кнопок в строке, а на выходе отдает саму клавиатуру
def create_inline_kb(dict_of_buttons, cnt_object_in_row):
    reply_to = types.InlineKeyboardMarkup(row_width = cnt_object_in_row)
    row = []
    for i in dict_of_buttons:
        current_button = types.InlineKeyboardButton(text = i, callback_data = dict_of_buttons[i])
        row.append(current_button)
        if len(row) == cnt_object_in_row:
            reply_to.add(*row)
            row = []
    reply_to.add(*row)
    return reply_to

#выдает сообщение с главным меню и кнопками выбора уровня JLPT.
def main_menu():
    text = 'Выбери уровень JLPT'
    cnt_object_in_row = 3
    dict_of_buttons = {"N5" : "5/", "N4" : "4/", "N3" : "3/", "N2" : "2/", "N1" : "1/", "Все уровни" : "-1/"}
    reply_to = create_inline_kb(dict_of_buttons, cnt_object_in_row)
    return text, reply_to

#выдает сообщение с меню выбора типа теста
def test_type(button_data):
    text = 'Выбери, как будем тестироваться'
    cnt_object_in_row = 1
    dict_of_buttons = {"По японскому чтению" : button_data + "1/", "По китайскому чтению" : button_data + "2/", "По переводу кандзи" : button_data + "3/", "В предыдущее меню" : "back_main"}
    reply_to = create_inline_kb(dict_of_buttons, cnt_object_in_row)
    return text, reply_to

#выдает сообщение с меню выбора количества вопросов в тесте
def cnt_questions_menu(button_data):
    text = 'Сколько вопросов?'
    cnt_object_in_row = 2
    dict_of_buttons = {"5" : button_data + "5/", "10" : button_data + "10/", "25" : button_data + "25/", "50" : button_data + "50/", "100" : button_data + "100/", "Все" : button_data + "-1/", "В предыдущее меню" : "back_main"}
    reply_to = create_inline_kb(dict_of_buttons, cnt_object_in_row)
    return text, reply_to

#выдает меню с кнопоками продолжить тест или вернуться в предыдщуее меню
def give_me_more(call):
    text = 'Вопрос отправлен'
    cnt_object_in_row = 1
    next_button = (call.data).replace("next", "") + "next"
    index = (call.data).rfind('/', 0, (call.data).rfind('/')) +1
    previous_menu = (call.data)[:index]
    dict_of_buttons = {"Далее" : next_button, "В предыдущее меню" : previous_menu}
    reply_to = create_inline_kb(dict_of_buttons, cnt_object_in_row)
    return text, reply_to

#выдает сообщение о том, что вопросы закончились и кнопки вернуться в предыдущее меню или главное меню
def questions_empty(call_data):
    text = 'Вопросы закончились'
    cnt_object_in_row = 1
    dict_of_buttons = {"В главное меню" : "back_main", "В предыдущее меню" : call_data}
    reply_to = create_inline_kb(dict_of_buttons, cnt_object_in_row)
    return text, reply_to
