import psycopg2
from config import host, user, db_name, password


def create():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database="postgres"
        )
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE procrastination_bli3_izhevsk")
        cursor.close()
        connection.close()
    except psycopg2.errors.DuplicateDatabase as _ex:
        pass
    except Exception as _ex:
        print("[INFO] Error while CREATING DATABASE", _ex)
