import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column

from dreamjob.config import settings
from structlog import get_logger

USER = settings.USER
PASSWORD = settings.PASSWORD
DB_CONNECTION_STRING = f"postgresql+psycopg2://{USER}:{PASSWORD}@localhost"

logger = get_logger()
# TODO: Add logging and exceptions, dynanconf secrets


def create_db():
    try:
        sql_engine = create_engine(DB_CONNECTION_STRING, isolation_level="AUTOCOMMIT")
        sql_engine.execute("CREATE DATABASE dreamjob")

        logger.info("Database 'dreamjob' has been created")

    except:
        logger.info("Database 'dreamjob' is ready to use")


def create_table():
    db_engine = create_engine(DB_CONNECTION_STRING + "/dreamjob")
    metadata = MetaData()

    employees = Table('employees', metadata,
                      Column('employee_id', sqlalchemy.Integer, primary_key=True),
                      Column('employee_name', sqlalchemy.String(60), nullable=False, key='name')
                      )
    employees.create(db_engine, checkfirst=True)

    logger.info("Table 'vacancies' is ready to use")

    employees_df = pd.read_sql_table("employees", db_engine)

    if employees_df.empty:
        logger.warning("There is no vacancies in table, add some with update_data.py")
    else:
        logger.info("Number of vacancies in table", number=employees_df.shape[0])
