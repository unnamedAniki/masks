from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TestConfig:
    SECRET_KEY = 'super_secret'
    POSTGRES_USER = 'user'
    POSTGRES_PASSWORD = 'password'
    POSTGRES_HOST = 'localhost'
    POSTGRES_PORT = 5432
    POSTGRES_DATABASE_NAME = 'chats'
    JWT_SECRET: str = 'secret'

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f"postgres+psycopg2://" + \
        f"{self.POSTGRES_USER}:" + \
        f"{self.POSTGRES_PASSWORD}@" + \
        f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/" + \
        f"{self.POSTGRES_DATABASE_NAME}"


engine = create_engine(TestConfig().SQLALCHEMY_DATABASE_URI)# echo=True)
db_session = sessionmaker(bind=engine)()
Base = declarative_base()
config = TestConfig()