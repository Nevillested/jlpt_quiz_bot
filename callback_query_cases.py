import keyboards
import queries_to_db

def main(MypyBot, call):

    #проверяем выбор уровня JLPT. N5 == 5, N4 == 4, N3 == 3, N2 == 2, N1 == 1, все уровни == -1
    if call.data in ['-1','1','2','3','4','5']:

        #получает сообщение с меню выбора количества вопросов в тесте
        text_out, reply_markup_out = keyboards.cnt_questions_menu(call.data)

        #отправляет сообщение
        MypyBot.send_message(call.message.chat.id, text_out, reply_markup = reply_markup_out)

    #проверяем выбор количества вопросов в тесте. Кнопка имеет вид: "3/50", где 3 - это уровень JLPT, а 50 - количество вопросов
    for prefix in ['-1/','1/','2/','3/','4/','5/','next/']:

        #если нажатая кнопка содержит и то и другое (то есть и уровень JLPT и кол-во вопросов в тесте), то...
        if call.data.startswith(prefix):

            #создаем переменную флага того, что пользователь нажал кнопку "далее", чтобы продолжить тест
            more_flg = None

            #создаем переменную, хранящуя уровень JLPT и количество вопросов
            call_data = None

            #если данные в кнопке содержат "next", значит пользователь нажал кнпопку далее и...
            if call.data.startswith('next/'):
                #...мы проставляем флаг и...
                more_flg = 1
                #...присваеиваем переменной, хранящей уровень JLPT и количество вопросов очищенные данные с уровнем JLPT и количеством вопросов
                call_data = (call.data).replace('next/','')
            #иначе...
            else:
                #...просто присваиваем переменной, хранящей уровень JLPT и количество вопросов обычные данные (тк они уже в чистом виде) с уровнем JLPT и количеством вопросов
                call_data = call.data

            #вытаскиваем из переменной, хранящей уровень JLPT и количество вопросов непосредственно уровень JLPT
            jlpt_lvl = (call_data.split('/'))[0]

            #вытаскиваем из переменной, хранящей уровень JLPT и количество вопросов непосредственно количество вопросов в тесте
            cnt_questions = (call_data.split('/'))[1]

            #если переменная флага с продолжением теста неактивна, то...
            if more_flg != 1:

                #генерируем для текущего пользователя список вопросов, на основе указанного количества и уровня JLPT
                queries_to_db.gen_questions(call.message.chat.id, cnt_questions, jlpt_lvl)

            #получаем из бд строки с данными для вопроса (квиза)
            poll_rows = queries_to_db.get_question(call.message.chat.id)

            #если пусто, значит вопросы закончились
            if len(poll_rows) == 0:

                #получаем сообщение с кнопкой вернуться назад
                text_out, reply_markup_out = keyboards.questions_empty(call.data)

                #отправляем сообщение с кнопкой вернуться назад
                MypyBot.send_message(call.message.chat.id, text_out, reply_markup = reply_markup_out)

            #в противном случае вопросы еще есть
            else:

                #объявляем переменную, которая будет в себе хранить номер вопроса
                question_num = None

                #объявляем переменную, чтобы понять на какой строке из полученнной выборки из бд находится верный ответ
                cnt = 0

                #объявляем массив с вариантами ответов
                poll_options = []

                #объявляем переменную, которая будет в себе хранить номер правильного ответа
                correct_id = None

                #объявляем переменную, которая будет в себе хранить сам вопрос
                question = None

                #проходимся по каждой строке
                for row in poll_rows:

                    #добавляем в массив варианты ответов
                    poll_options.append(row[1])

                    #row[2] это третий столбец. Третий столбец это столбец, который в себе хранит флаг правильного ответа. Если третий столбец текущей строки равен 1, значит это строка хранит в себе данные по верному ответу
                    if row[2] == 1:

                        #хапоминаем номер правильного ответа
                        correct_id = cnt

                        #запоминаем сам вопрос
                        question = row[0]

                        #запоминаем номер вопроса
                        question_num = row[3]

                    #инкрментируем переменную, чтобы понять на какой строке из полученнной выборки из бд находится верный ответ
                    cnt += 1

                #отправляем сам вопрос (квиз)
                MypyBot.send_poll(call.message.chat.id, question, options = poll_options, correct_option_id  = correct_id, type = 'quiz')

                #запоминаем в бд, что этот вопрос уже отправлен
                queries_to_db.update_question(call.message.chat.id, question_num)

                #получаем текст с кнопкой о предложении продолжить тестирование или вернуться назад
                text_out, reply_markup_out = keyboards.give_me_more(call_data)

                #отправляем текст с кнопкой о предложении продолжить тестирование или вернуться назад
                MypyBot.send_message(call.message.chat.id, text_out, reply_markup = reply_markup_out)

            #выходим из цикла, чтобы в холостую не гонять по циклу
            break

    #кнопка, возвращающая в главное меню
    if call.data == "back_main":

        #получает сообщение с кнопками для главного меню
        text_out, reply_markup_out = keyboards.main_menu()

        #отправляет сообщение с кнопками для главного меню
        MypyBot.send_message(call.message.chat.id, text_out, reply_markup = reply_markup_out)