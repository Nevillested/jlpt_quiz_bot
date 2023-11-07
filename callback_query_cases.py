import keyboards
import queries_to_db

def main(MypyBot, call):

    poll_options = []
    correct_id = None
    question = None

    if call.data in ['-1','1','2','3','4','5']:
        text_out, reply_markup_out = keyboards.cnt_questions_menu(call.data)
        MypyBot.send_message(call.message.chat.id, text_out, reply_markup = reply_markup_out)

    for prefix in ['-1/','1/','2/','3/','4/','5/', 'more/']:

        more_flg = None
        call_data = None
        if call.data.startswith('more/'):
            more_flg = 1
            call_data = (call.data).replace('more/','')
        else:
            call_data = call.data

        if call.data.startswith(prefix):
            jlpt_lvl = (call_data.split('/'))[0]
            cnt_questions = (call_data.split('/'))[1]

            if more_flg != 1:
                queries_to_db.gen_questions(call.message.chat.id, cnt_questions, jlpt_lvl)

            poll_rows = queries_to_db.get_question(call.message.chat.id)

            if len(poll_rows) > 0:
                question_num_array = []
                cnt = 0
                for row in poll_rows:
                    poll_options.append(row[1])
                    question_num_array.append(row[3])

                    if row[2] == 1:
                        correct_id = cnt
                        question = row[0]

                    cnt += 1
                unique_question_num = set(question_num_array)
                unique_list = list(unique_question_num)
                question_num = unique_list[0]
                MypyBot.send_poll(call.message.chat.id, question, options = poll_options, correct_option_id  = correct_id, type = 'quiz')
                queries_to_db.update_question(call.message.chat.id, question_num)
                text_out, reply_markup_out = keyboards.give_me_more(call_data)
                MypyBot.send_message(call.message.chat.id, text_out, reply_markup = reply_markup_out)
            else:
                MypyBot.send_message(call.message.chat.id, 'Вопросы закончились:( /menu')


            break
