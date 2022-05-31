from structlog import get_logger

from dreamjob.backend.db.collect_data_hh import get_vacancies
from dreamjob.backend.db.preprocess_data import preprocess_data
from dreamjob.backend.db.data_manipulation import insert
from dreamjob.backend.db.db_engine import DBConfig

logger = get_logger()


def add_new_vacancies(area: int, period: int, per_page: int, db_engine=None) -> None:
    """Periodically upgrade table with new vacancies

    Period - each day in the morning
    TODO: Add celery task
    TODO: Call DB_CONNECTION_STRING once
    """
    db_engine = db_engine if db_engine is not None else DBConfig.get().db_engine

    vacancies_raw = get_vacancies(
        area=area, period=period, per_page=per_page
    )
    vacancies = preprocess_data(vacancies_raw)
    number_of_new_vacs = insert(vacancies, db_engine)

    logger.info("New vacancies were added to table",
                number_of_new_vacs=number_of_new_vacs)
