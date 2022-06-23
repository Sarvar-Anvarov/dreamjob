import sqlalchemy
from dreamjob.config import settings

USER = settings.USER
PASSWORD = settings.PASSWORD
DB_CONNECTION_STRING = f"postgresql+psycopg2://{USER}:{PASSWORD}@localhost/dreamjob"


class DBConfig:

    _instance = None

    def __init__(self, db_engine):
        self.db_engine = db_engine

    @classmethod
    def get(cls):
        if not cls._instance:
            db_engine = sqlalchemy.create_engine(DB_CONNECTION_STRING)
            cls._instance = cls(db_engine)
        return cls._instance
