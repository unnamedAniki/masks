from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import connect
from sqlalchemy import create_engine


class DBConnect:
    def __init__(self):

        connection = connect(user="postgres", password="postgres")
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Создаем курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        cursor.execute('create database sqlalchemy_tuts')

        cursor.close()
        connection.close()
        self.engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost/logs", echo=True)