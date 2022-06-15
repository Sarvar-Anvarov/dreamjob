import time
import schedule
from schedule import every, repeat

from typing import Dict
from structlog import get_logger

from dreamjob.backend.db.collect_data_hh import get_vacancies
from dreamjob.backend.db.preprocess_data import preprocess_data
from dreamjob.backend.db.data_manipulation import insert
from dreamjob.backend.db.db_engine import DBConfig
from dreamjob.backend.commons.exceptions import DataCollectionFailed

logger = get_logger()


@repeat(every().day.at("00:00"))
def add_new_vacancies(area: int = 2,
                      period: int = 1,
                      per_page: int = 100) -> Dict[str, str]:
    """
    Periodically update table with new vacancies
    Period - each day in the morning
    TODO: Add celery task
    """
    try:
        logger.info("Add new vacancies",
                    area=area, period=period, per_page=per_page)

        db_engine = DBConfig.get().db_engine

        vacancies_raw = get_vacancies(area=area, period=period, per_page=per_page)
        vacancies = preprocess_data(vacancies_raw)
        number_of_new_vacs = insert(vacancies, db_engine)

        logger.info("New vacancies were added to table",
                    number_of_new_vacs=number_of_new_vacs)

        return {"status": f"{number_of_new_vacs} new vacancies were added"}

    except DataCollectionFailed:
        logger.info("Data collection failed")


# Not the best way to do a periodic job
while True:
    schedule.run_pending()
    time.sleep(1)
