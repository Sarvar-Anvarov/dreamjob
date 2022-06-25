import pickle
from structlog import get_logger

from dreamjob.config import settings
from dreamjob.ml.models.tf_idf import TFIDFModel

logger = get_logger()


def choose_vacancies(user_input):
    model = pickle.load(open(settings.TF_IDF.model, "rb"))
    matrix = pickle.load(open(settings.TF_IDF.matrix, "rb"))

    recommender = TFIDFModel(model)
    idx = recommender.predict(user_input.lower(), matrix)

    # logger.info("User input", user_input=user_input)
    print(user_input, idx)

    return idx
