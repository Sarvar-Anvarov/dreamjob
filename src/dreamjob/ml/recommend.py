from structlog import get_logger
from dreamjob.ml.models.base import BaseModel

logger = get_logger()


def choose_vacancies(user_input, recommender: BaseModel):
    recommender.load_artifacts()
    idx = recommender.predict(user_input.lower())

    return idx
