import psycopg2
import config
import random

conn = psycopg2.connect(config.pg_sql_con_string)
conn.autocommit = True
cur = conn.cursor()

#процедура удаляет все данные из таблицы и наполняет ее заново на основе того количества вопросов и уровня JLPT, которое выбрал пользователь
def gen_questions(chat_id, cnt_questions, jlpt_level):
    cur.execute(""" call jlpt_quiz_bot.gen_users_questions_data(""" + str(chat_id) + """, """ + str(cnt_questions) + """, """ + str(jlpt_level) + """); """)

#получает данные для квиза, которые еще не были отправлены
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

#проставляет в таблице с вопросами для пользователя флаг о том, что вопрос отправлен, чтобы повторно его не отправить
def update_question(chat_id, question_num):
    cur_text = """update jlpt_quiz_bot.users_questions
                     set sent_flg = 1
                   where chat_id = """ + str(chat_id) + """
                     and question_num = """ + str(question_num) + """
    """
    cur.execute(cur_text)
