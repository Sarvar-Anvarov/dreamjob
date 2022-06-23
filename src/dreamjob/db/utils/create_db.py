import datetime
import sqlalchemy
import pandas as pd

from sqlalchemy import create_engine, MetaData
from structlog import get_logger

from dreamjob.config import settings
from .engine import DBConfig

USER = settings.USER
PASSWORD = settings.PASSWORD
DB_CONNECTION_STRING = f"postgresql+psycopg2://{USER}:{PASSWORD}@localhost/"

logger = get_logger()


def create_db():
    try:
        sql_engine = create_engine(DB_CONNECTION_STRING, isolation_level="AUTOCOMMIT")
        sql_engine.execute("CREATE DATABASE dreamjob")

    except Exception as e:
        logger.info("Database 'dreamjob' already exists", msg=e.__class__.__name__)


def create_table(db_engine=None):
    db_engine = db_engine if db_engine is not None else DBConfig.get().db_engine
    metadata = MetaData()

    vacancies = sqlalchemy.Table(
        "vacancies",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, unique=True),
        sqlalchemy.Column("premium", sqlalchemy.Boolean),
        sqlalchemy.Column("name", sqlalchemy.String),
        sqlalchemy.Column("description", sqlalchemy.String),
        sqlalchemy.Column("key_skills", sqlalchemy.ARRAY(sqlalchemy.String)),
        sqlalchemy.Column("accept_handicapped", sqlalchemy.Boolean),
        sqlalchemy.Column("accept_kids", sqlalchemy.Boolean),
        sqlalchemy.Column("archived", sqlalchemy.Boolean),
        sqlalchemy.Column("specializations", sqlalchemy.ARRAY(sqlalchemy.String)),
        sqlalchemy.Column("professional_roles", sqlalchemy.String),
        sqlalchemy.Column("published_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow),
        sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow),
        sqlalchemy.Column("alternate_url", sqlalchemy.String),
        sqlalchemy.Column("billing_type.id", sqlalchemy.String),
        sqlalchemy.Column("billing_type.name", sqlalchemy.String),
        sqlalchemy.Column("experience.id", sqlalchemy.String),
        sqlalchemy.Column("experience.name", sqlalchemy.String),
        sqlalchemy.Column("schedule.id", sqlalchemy.String),
        sqlalchemy.Column("schedule.name", sqlalchemy.String),
        sqlalchemy.Column("employment.id", sqlalchemy.String),
        sqlalchemy.Column("employment.name", sqlalchemy.String),
        sqlalchemy.Column("employer.id", sqlalchemy.Integer),
        sqlalchemy.Column("employer.name", sqlalchemy.String),
        sqlalchemy.Column("employer.url", sqlalchemy.String),
        sqlalchemy.Column("employer.alternate_url", sqlalchemy.String),
        sqlalchemy.Column("employer.logo_urls.original", sqlalchemy.String),
        sqlalchemy.Column("employer.logo_urls.240", sqlalchemy.String),
        sqlalchemy.Column("employer.logo_urls.90", sqlalchemy.String),
        sqlalchemy.Column("employer.vacancies_url", sqlalchemy.String),
        sqlalchemy.Column("employer.trusted", sqlalchemy.Boolean),
        sqlalchemy.Column("address.city", sqlalchemy.String),
        sqlalchemy.Column("address.street", sqlalchemy.String),
        sqlalchemy.Column("address.building", sqlalchemy.String),
        sqlalchemy.Column("address.description", sqlalchemy.String),
        sqlalchemy.Column("address.lat", sqlalchemy.Float),
        sqlalchemy.Column("address.lng", sqlalchemy.Float),
        sqlalchemy.Column("address.raw", sqlalchemy.String),
        sqlalchemy.Column("salary.currency", sqlalchemy.String),
        sqlalchemy.Column("salary.from", sqlalchemy.Float),
        sqlalchemy.Column("salary.to", sqlalchemy.Float),
        sqlalchemy.Column("salary.gross", sqlalchemy.Boolean),
    )
    vacancies.create(db_engine, checkfirst=True)

    logger.info("Table 'vacancies' is ready to use")

    vacancies_df = pd.read_sql_table("vacancies", db_engine)

    if vacancies_df.empty:
        logger.warning("There is no vacancies in table, add some with update_data.py")
    else:
        logger.info("Number of vacancies in table", number=vacancies_df.shape[0])
