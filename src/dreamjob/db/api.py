import os
from sqlalchemy import create_engine
from structlog import get_logger

from dreamjob.db.collect_data_hh import get_vacancies
from dreamjob.db.preprocess_data import preprocess_data
from dreamjob.db.data_manipulation import insert
from dreamjob.db.create_db import DB_CONNECTION_STRING

logger = get_logger()


def add_new_vacancies(area, period, per_page):
    """Periodically upgrade table with new vacancies

    Period - each day in the morning
    TODO: Add celery task
    TODO: Call DB_CONNECTION_STRING once
    """
    db_engine = create_engine(os.path.join(DB_CONNECTION_STRING, "dreamjob"))

    vacancies_raw = get_vacancies(
        area=area, period=period, per_page=per_page
    )
    vacancies = preprocess_data(vacancies_raw)
    number_of_new_vacs = insert(vacancies, db_engine)

    logger.info("New vacancies were added to table",
                number_of_new_vacs=number_of_new_vacs)
