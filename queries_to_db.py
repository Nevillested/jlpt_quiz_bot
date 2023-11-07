import psycopg2
import config
import random

conn = psycopg2.connect(config.pg_sql_con_string)
conn.autocommit = True
cur = conn.cursor()

def get_poll(jlpt_lvl):
    additional_filter = None
    if jlpt_lvl != '6':
        additional_filter = " and jlpt_level = " + jlpt_lvl
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
    correct_id = None
    dict_of_kanji = {}
    key = 0
    for option in rows:
        poll_options.append(option[2])
        dict_of_kanji[key] = option[0]
        key += 1
    for key, value in dict_of_kanji.items():
        if value == true_id:
            correct_id = key
            break

    return poll_options, correct_id, question

def gen_questions(chat_id, cnt_questions, jlpt_level):
    cur.execute(""" call jlpt_quiz_bot.gen_users_questions_data(""" + str(chat_id) + """, """ + str(cnt_questions) + """, """ + str(jlpt_level) + """); """)

def get_question(chat_id):
    cur_text = """select question_txt,
                         answers,
                         flg_true_answer,
                         question_num
                    from jlpt_quiz_bot.users_questions
                   where sent_flg = 0
                     and chat_id = """ + str(chat_id) + """
                   order by question_num asc
                   limit 4
    """
    cur.execute(cur_text)
    rows = cur.fetchall()
    return rows

def update_question(chat_id, question_num):
    cur_text = """update jlpt_quiz_bot.users_questions
                     set sent_flg = 1
                   where chat_id = """ + str(chat_id) + """
                     and question_num = """ + str(question_num) + """
    """
    cur.execute(cur_text)
