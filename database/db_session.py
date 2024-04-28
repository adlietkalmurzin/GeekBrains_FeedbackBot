import datetime
from datetime import timezone
from io import BytesIO

import psycopg2
import xlsxwriter as xs
from PIL import Image

from analytics.analytics import get_all_plots
from database.config import host, user, db_name, password
from database.create_db import create_db

create_db()

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
        user_id BIGINT,
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
    cells = {0: 'A', 1: 'F'}
    offset = {1: -80, 0: 0}
    header = ('Время', 'Вопрос 1', 'Вопрос 2', 'Вопрос 3', 'Вопрос 4', 'Вопрос 5', 'релевантен ли отзыв',
              'к кому направлен отзыв', 'позитивен ли отзыв')
    cursor.execute("SELECT * FROM feedback ORDER BY feedback.time")
    xlsx = BytesIO()
    workbook = xs.Workbook(xlsx)
    worksheet = workbook.add_worksheet()
    db_data = cursor.fetchall()
    for i, row in enumerate(header):
        worksheet.set_column(i, i, 20)
        worksheet.write(0, i, row)
    for i, row in enumerate(db_data):
        for j, data in enumerate(row):
            if j == 7:
                worksheet.write(i + 1, j, obj[data])
            elif j == 6 or j == 8:
                worksheet.write(i + 1, j, yes_no[data])
            elif j == 0:
                worksheet.write(i + 1, j, str(data))
            else:
                worksheet.write(i + 1, j, data)
    for k, plot in enumerate(get_all_plots(db_data)):
        if k <= 7:
            plot = crop_image(plot)
            worksheet.insert_image(f"{cells[k % 2]}{i + 7 + 28 * (k // 2)}", 'plot.png',
                                   {"image_data": plot, "x_scale": 0.38, "y_scale": 0.5, "x_offset": offset[k % 2]})
        else:
            worksheet.insert_image(f"{cells[k % 2]}{i + 7 + 28 * (k // 2)}", 'plot.png',
                                   {"image_data": plot, "x_scale": 0.38, "y_scale": 0.5})
    workbook.close()
    xlsx.seek(0)
    return xlsx


def get_plots():
    cursor.execute("SELECT * FROM feedback ORDER BY feedback.time")
    data = cursor.fetchall()
    return get_all_plots(data)


def send_user_to_base(user_id, first_name, last_name, user_type):
    cursor.execute("INSERT INTO users VALUES(%s, %s, %s, %s)", (user_id, first_name, last_name, user_type))


def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    if result is None:
        return None
    return result[1:]


def crop_image(image_bytes, new_size=(1700, 1100)):
    img = Image.open(image_bytes)

    if new_size is None:
        new_size = (img.width, img.height)

    left = (img.width - new_size[0]) // 2
    top = (img.height - new_size[1]) // 2
    right = (img.width + new_size[0]) // 2
    bottom = (img.height + new_size[1]) // 2

    cropped_img = img.crop((left, top, right, bottom))

    img_byte_arr = BytesIO()
    cropped_img.save(img_byte_arr, format='PNG')
    return img_byte_arr
