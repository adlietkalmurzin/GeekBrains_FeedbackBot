import datetime

import psycopg2
from config import host, user, db_name, password
from create_db import create
from datetime import timezone
import xlsxwriter as xs
from io import BytesIO

create()

conn = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name
)
conn.autocommit = True
cursor = conn.cursor()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS feedback(
        time timestamp,
        question_1 TEXT,
        question_2 TEXT,
        question_3 TEXT,
        question_4 TEXT,
        question_5 TEXT,
        is_relevant BOOL,
        object INTEGER,
        is_positive BOOL);"""
)
cursor.execute(
    """CREATE TABLE IF NOT EXISTS train_data(
        time timestamp,
        question_1 TEXT,
        question_2 TEXT,
        question_3 TEXT,
        question_4 TEXT,
        question_5 TEXT,
        is_relevant BOOl,
        object INTEGER,
        is_positive BOOL);"""
)
cursor.execute(
    """CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER,
        first_name TEXT,
        last_name TEXT,
        user_type INTEGER);"""
)


def send_to_train(q1, q2, q3, q4, q5, is_relevant, object_, is_positive):
    msk = timezone(datetime.timedelta(hours=3))
    timestamp = datetime.datetime.now(msk).replace(microsecond=0).isoformat(' ')

    cursor.execute("""INSERT INTO train_data VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (timestamp, q1, q2, q3, q4, q5, bool(is_relevant), object_, bool(is_positive)))


def send_to_feedback(q1, q2, q3, q4, q5, is_relevant, object_, is_positive):
    msk = timezone(datetime.timedelta(hours=3))
    timestamp = datetime.datetime.now(msk).replace(microsecond=0).isoformat(' ')

    cursor.execute("""INSERT INTO feedback VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (timestamp, q1, q2, q3, q4, q5, bool(is_relevant), object_, bool(is_positive)))


def send_to_base(q1, q2, q3, q4, q5, is_relevant, object_, is_positive):
    send_to_train(q1, q2, q3, q4, q5, is_relevant, object_, is_positive)
    if is_relevant:
        send_to_feedback(q1, q2, q3, q4, q5, is_relevant, object_, is_positive)


def get_table():
    yes_no = {1: 'Да', 0: 'Нет'}
    obj = {0: 'вебинар', 1: 'программа', 2: 'преподаватель'}
    header = ('Время', 'Вопрос 1', 'Вопрос 2', 'Вопрос 3', 'Вопрос 4', 'Вопрос 5', 'релевантен ли отзыв',
              'к кому направлен отзыв', 'позитивен ли отзыв')
    cursor.execute("SELECT * FROM feedback")
    xlsx = BytesIO()
    workbook = xs.Workbook(xlsx)
    worksheet = workbook.add_worksheet()
    for i, row in enumerate(header):
        worksheet.set_column(i, i, 20)
        worksheet.write(0, i, row)
    for i, row in enumerate(cursor.fetchall()):
        for j, data in enumerate(row):
            if j == 7:
                worksheet.write(i + 1, j, obj[data])
            elif j == 6 or j == 8:
                worksheet.write(i + 1, j, yes_no[data])
            elif j == 0:
                worksheet.write(i + 1, j, str(data))
            else:
                worksheet.write(i + 1, j, data)

    workbook.close()
    xlsx.seek(0)
    return xlsx


def send_user_to_base(user_id, first_name, last_name, user_type):
    cursor.execute("INSERT INTO users VALUES(%s, %s, %s, %s)", (user_id, first_name, last_name, user_type))


def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    return cursor.fetchone()


with open("output.xlsx", "wb") as f:
    f.write(get_table().getbuffer())
# send_to_base('asdfsa', 'asdfsa', 'asdfsa', 'asdfsa', 'asdfsa', 1, 2, 1)
# cursor.execute("SELECT * FROM feedback")
# print(str(cursor.fetchall()[0][0]))
