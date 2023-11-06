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

############################# клавиатура основного меню #############################
def main_menu():
    text = 'Выбери уровень JLPT'
    cnt_object_in_row = 3
    dict_of_buttons = {"N5" : "5", "N4" : "4", "N3" : "3", "N2" : "2", "N1" : "1", "Все уровни" : "6"}
    reply_to = create_inline_kb(dict_of_buttons, cnt_object_in_row)
    return text, reply_to