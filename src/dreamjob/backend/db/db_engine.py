import os
import sqlalchemy
from dreamjob.backend.config import settings

DB_CONNECTION_STRING = os.path.join(settings.DB_CONNECTION_STRING, "dreamjob")


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
