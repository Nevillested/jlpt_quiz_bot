import telebot
import config
import keyboards
import callback_query_cases

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
    callback_query_cases.main(MypyBot, call)

#могут быть ошибки связи с сервером, поэтому бот будет перезапускаться каждый раз при ошибках
def start_bot():
    while True:
        try:
            print('Запуск бота')
            MypyBot.polling()
        except:
            print('ошибка')
            time.sleep(5)
#запускаем бота
start_bot()