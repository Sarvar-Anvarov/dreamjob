from celery import Celery
from celery.schedules import crontab
from structlog import get_logger

from .utils.collect_data import get_vacancies
from .utils.preprocess_data import preprocess_data
from .utils.data_manipulation import insert, select
from .utils.engine import DBConfig
from dreamjob.commons.exceptions import DataCollectionFailed

logger = get_logger()
app = Celery('tasks', broker='redis://localhost//')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Executes every day at 00:00 UTC
    sender.add_periodic_task(
        crontab(hour=0, minute=0),
        add_new_vacancies.s(),
        name="add new vacancies",
    )


@app.task
def add_new_vacancies(area: int = 2,
                      period: int = 1,
                      per_page: int = 100) -> None:
    """
    Periodically update table with new vacancies
    Period - every day at 00:00 UTC
    """
    try:
        logger.info("Add new vacancies",
                    area=area, period=period, per_page=per_page)

        db_engine = DBConfig.get().db_engine

        # parse vacancies and preprocess data
        vacancies_raw = get_vacancies(area=area, period=period, per_page=per_page)
        vacancies = preprocess_data(vacancies_raw.dropna(subset=["id"]))

        # check if vacancy is in database already
        ids_in_db = select(columns="id", engine=db_engine)["id"].astype("str")
        vacancies_to_insert = vacancies.query("id not in @ids_in_db")
        vacancies_to_update = vacancies.query("id in @ids_in_db")

        logger.info("Number of already existing ids",
                    number_of_existing_ids=ids_in_db.shape[0])

        # insert new vacancies
        number_of_new_vacs = insert(vacancies_to_insert, db_engine)

        logger.info("New vacancies were added to table",
                    number_of_new_vacs=number_of_new_vacs,
                    number_of_vacs_to_update=vacancies_to_update.shape[0])

    except DataCollectionFailed:
        logger.info("Data collection failed")
