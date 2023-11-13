import keyboards
import queries_to_db

def get_and_send_question(MypyBot, call):
    #получаем из бд строки с данными для вопроса (квиза)
    poll_rows = queries_to_db.get_question(call.message.chat.id)

    #если пусто, значит вопросы закончились
    if len(poll_rows) == 0:

        #вытаскиваем предыдущее меню
        index = (call.data).rfind('/', 0, (call.data).rfind('/')) + 1
        previous_menu = (call.data)[:index]

        #получаем сообщение с кнопкой вернуться назад
        text_out, reply_markup_out = keyboards.questions_empty(previous_menu)

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

                #запоминаем номер правильного ответа
                correct_id = cnt

                #запоминаем сам вопрос
                question = row[0]

                #запоминаем номер вопроса
                question_num = row[3]

            #инкрментируем переменную, чтобы понять на какой строке из полученнной выборки из бд находится верный ответ
            cnt += 1

        #отправляем сам вопрос (квиз)
        MypyBot.send_poll(call.message.chat.id, 'Вопрос №' + str(question_num) + '.' + question, options = poll_options, correct_option_id  = correct_id, type = 'quiz')

        #запоминаем в бд, что этот вопрос уже отправлен
        queries_to_db.update_question(call.message.chat.id, question_num)

        #получаем текст с кнопкой о предложении продолжить тестирование или вернуться назад
        text_out, reply_markup_out = keyboards.give_me_more(call)

        #отправляем текст с кнопкой о предложении продолжить тестирование или вернуться назад
        MypyBot.send_message(call.message.chat.id, text_out, reply_markup = reply_markup_out)

def main(MypyBot, call):

    #кнопка, возвращающая в главное меню
    if call.data == "back_main":

        #получает сообщение с кнопками для главного меню
        text_out, reply_markup_out = keyboards.main_menu()

        #отправляет сообщение с кнопками для главного меню
        MypyBot.send_message(call.message.chat.id, text_out, reply_markup = reply_markup_out)

    #данные в кнопке обязательно должны быть разделены символом /.Так мы будем понимать, какие кнопки пользователь нажал ранее
    #Если данные в кнопке не содержат символа /, то юзер нажал либо кнпоку "back_main" - главное меню, либо "next" - продолжить тест
    elif '/' in (call.data):

        #создаем массив из данных, которые были в кнопке. Первый элемент массива будет - уровень JLPT; второй - тип теста, третий - количество вопросов в тесте
        array_of_menu_id = (call.data).split('/')

        #удаляем пустые значения из массива
        array_of_menu_id = list(filter(None, array_of_menu_id))

        #Если длина массива == 1, значит был выбран только уровень JLPT, где: N5 == 5, N4 == 4, N3 == 3, N2 == 2, N1 == 1, все уровни == -1
        if len(array_of_menu_id) == 1:

            #получает сообщение с меню выбора типа теста
            text_out, reply_markup_out = keyboards.test_type(call.data)

            #отправляет сообщение
            MypyBot.send_message(call.message.chat.id, text_out, reply_markup = reply_markup_out)


        #Если длина массива == 2, значит был выбран тип теста, где 1 - тест по японскому чтению, 2 - тест по китайскому чтению, 3 - тест по переводу
        elif len(array_of_menu_id) == 2:

            #получает сообщение с меню выбора количества вопросов в тесте
            text_out, reply_markup_out = keyboards.cnt_questions_menu(call.data)

            #отправляет сообщение
            MypyBot.send_message(call.message.chat.id, text_out, reply_markup = reply_markup_out)

        #если длина массива == 3, значит было выбрано количество вопросов, где 5 - 5 вопросов, 10 - 10 вопросов, 25 - 50 вопросов, 100 - 100 вопросов, -1 - все вопросы
        elif len(array_of_menu_id) == 3:

            #вытаскиваем из переменной, хранящей уровень JLPT и количество вопросов непосредственно уровень JLPT
            jlpt_lvl = ((call.data).split('/'))[0]

            #вытаскиваем из переменной, хранящей тип теста непсоредственно сам тип теста
            test_type = ((call.data).split('/'))[1]

            #вытаскиваем из переменной, хранящей уровень JLPT и количество вопросов непосредственно количество вопросов в тесте
            cnt_questions = ((call.data).split('/'))[2]

            #отправляем сообщение с просьбой подождать, тк генерация может занимать какое-то время
            MypyBot.send_message(call.message.chat.id, 'Немного терпения, генерируем вопросы..')

            #генерируем для текущего пользователя список вопросов, на основе указанного количества, уровня JLPT и типа тестирования
            queries_to_db.gen_questions(call.message.chat.id, jlpt_lvl, test_type, cnt_questions)

            #получаем и отправляем вопрос
            get_and_send_question(MypyBot, call)

        #если длина массива == 4, то тут только 1 вариант, что помимо уровня JLPT, типа теста, кол-ва вопросов еще есть слово next, в самом конце - что значит пользователь попросил следующий вопрос
        elif len(array_of_menu_id) == 4:

            #получаем и отправляем вопрос
            get_and_send_question(MypyBot, call)