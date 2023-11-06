import telebot
import config
import keyboards
import time
import psycopg2
import random

MypyBot = telebot.TeleBot(config.telegram_token)

CONTENT_TYPES = ["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact", "pinned_message"]

@MypyBot.message_handler(content_types=CONTENT_TYPES)
def start_message(message):
    print(f"Пришло сообщение от: {message.from_user.username}\nТип сообщения: {str(message.content_type)}\nТекст сообщения: {message.text}\n")
    text_out, reply_markup_out = keyboards.main_menu()
    MypyBot.send_message(message.chat.id, text_out, reply_markup = reply_markup_out)

#хэндлер нажатий на кнопки
@MypyBot.callback_query_handler(func=lambda call: True)
def start_callback_query(call):
    print(f"{call.from_user.username} нажал кнопку {call.data}.\n")
    MypyBot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)

    if call.data in ['6','5','4','3','2','1']:
        conn = psycopg2.connect(config.pg_sql_con_string)
        conn.autocommit = True
        cur = conn.cursor()
        additional_filter = None
        if call.data != '6':
            additional_filter = " and jlpt_level = " + call.data
        cur_text = """select id,
                             'Что это за кадзи ' || kanji || '?',
                             rus_translate
                         from jlpt_quiz_bot.kanji
                        where 1 = 1 """ + additional_filter + """
                        ORDER BY random()
                        limit 4"""
        cur.execute(cur_text)
        rows = cur.fetchall()
        true_row = random.choice(rows)
        true_id = true_row[0]
        question = true_row[1]
        poll_options = []
        dict_of_kanji = {}
        key = 0
        for option in rows:
            poll_options.append(option[2])
            dict_of_kanji[key] = option[0]
            key += 1
        correct_id = None
        for key, value in dict_of_kanji.items():
            if value == true_id:
                correct_id = key
                break
        MypyBot.send_poll(call.message.chat.id, question, options = poll_options, correct_option_id  = correct_id, type = 'quiz')


#могут быть ошибки связи с сервером, поэтому бот будет перезапускаться каждый раз при ошибках
def start_bot():
    while True:
        #try:
            print('Запуск бота')
            MypyBot.polling()
        #except:
        #    print('ошибка')
        #    time.sleep(5)
#запускаем бота
start_bot()