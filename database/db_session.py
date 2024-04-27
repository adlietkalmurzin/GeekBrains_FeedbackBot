import datetime
from datetime import timezone
from io import BytesIO

import psycopg2
import xlsxwriter as xs
from PIL import Image

from analytics.analytics import get_all_pn_plot, get_specifically_pn_plot, get_all_obj_all_rew_plot, \
    plot_positive_or_negative_reviews_ratio
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
    worksheet.insert_image("A10", 'plotik.png',
                           {"image_data": crop_image(get_all_pn_plot()), "x_scale": 0.38, "y_scale": 0.5})
    worksheet.insert_image("F10", 'plotik.png',
                           {"image_data": crop_image(get_all_pn_plot(True)), "x_scale": 0.38, "y_scale": 0.5,
                            "x_offset": -80})
    worksheet.insert_image("A38", 'plotik.png',
                           {"image_data": crop_image(get_specifically_pn_plot(0, )), "x_scale": 0.38,
                            "y_scale": 0.5})
    worksheet.insert_image("F38", 'plotik.png',
                           {"image_data": crop_image(get_specifically_pn_plot(0, True)), "x_scale": 0.38,
                            "y_scale": 0.5,
                            "x_offset": -80})
    worksheet.insert_image("A66", 'plotik.png',
                           {"image_data": crop_image(get_specifically_pn_plot(1)), "x_scale": 0.38,
                            "y_scale": 0.5})
    worksheet.insert_image("F66", 'plotik.png',
                           {"image_data": crop_image(get_specifically_pn_plot(1, True)), "x_scale": 0.38,
                            "y_scale": 0.5,
                            "x_offset": -80})
    worksheet.insert_image("A94", 'plotik.png',
                           {"image_data": crop_image(get_specifically_pn_plot(2)), "x_scale": 0.38, "y_scale": 0.5})
    worksheet.insert_image("F94", 'plotik.png',
                           {"image_data": crop_image(get_specifically_pn_plot(2, True)), "x_scale": 0.38,
                            "y_scale": 0.5,
                            "x_offset": -80})
    worksheet.insert_image("A122", 'plotik.png',
                           {"image_data": get_all_obj_all_rew_plot(), "x_scale": 0.38, "y_scale": 0.5})
    worksheet.insert_image("F122", 'plotik.png',
                           {"image_data": get_all_obj_all_rew_plot(True), "x_scale": 0.38, "y_scale": 0.5})
    worksheet.insert_image("A150", 'plotik.png',
                           {"image_data": plot_positive_or_negative_reviews_ratio(), "x_scale": 0.38, "y_scale": 0.5})
    worksheet.insert_image("F150", 'plotik.png',
                           {"image_data": plot_positive_or_negative_reviews_ratio(True), "x_scale": 0.38,
                            "y_scale": 0.5})
    workbook.close()
    xlsx.seek(0)
    return xlsx


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


