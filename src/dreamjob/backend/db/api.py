import time
import schedule
from schedule import every, repeat

from structlog import get_logger

from dreamjob.backend.db.collect_data import get_vacancies
from dreamjob.backend.db.preprocess_data import preprocess_data
from dreamjob.backend.db.data_manipulation import insert, select
from dreamjob.backend.db.engine import DBConfig
from dreamjob.backend.commons.exceptions import DataCollectionFailed

logger = get_logger()


@repeat(every().day.at("00:00"))
def add_new_vacancies(area: int = 2,
                      period: int = 1,
                      per_page: int = 100) -> None:
    """
    Periodically update table with new vacancies
    Period - each day in the morning
    TODO: Add celery task
    """
    try:
        logger.info("Add new vacancies",
                    area=area, period=period, per_page=per_page)

        db_engine = DBConfig.get().db_engine

        # parse vacancies and preprocess data
        vacancies_raw = get_vacancies(area=area, period=period, per_page=per_page)
        vacancies = preprocess_data(vacancies_raw)

        # check if vacancy is in database already
        ids_in_db = select(columns="id", engine=db_engine)["id"]
        vacancies_to_insert = vacancies.query("id not in @ids_in_db")
        vacancies_to_update = vacancies.query("id in @ids_in_db")

        # insert new vacancies
        number_of_new_vacs = insert(vacancies_to_insert, db_engine)

        logger.info("New vacancies were added to table",
                    number_of_new_vacs=number_of_new_vacs,
                    number_of_vacs_to_update=vacancies_to_update.shape[0])

    except DataCollectionFailed:
        logger.info("Data collection failed")


# TODO: not working, CELERY-CELERY-CELERY
# Not the best way to do a periodic job
while True:
    schedule.run_pending()
    time.sleep(1)
