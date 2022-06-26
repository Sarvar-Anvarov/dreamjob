import uvicorn
from fastapi import FastAPI

from dreamjob.db.utils.create_db import create_db, create_table
from dreamjob.ml.recommend import choose_vacancies
from dreamjob.ml.models.tf_idf import TFIDFModel
from dreamjob.commons.data_models import Recommendations, RecommendationRequest
from dreamjob.logger import setup_logging
from dreamjob.config import settings

LOG_DIR = settings.LOG_DIR

app = FastAPI()


@app.get("/")
def read_root():
    return {"status": "ok"}


@app.on_event("startup")
def startup_events():
    setup_logging(LOG_DIR)
    create_db()
    create_table()


@app.post("/recommend", response_model=Recommendations)
def recommend(request: RecommendationRequest):
    vacancies = choose_vacancies(
        user_input=request.user_input,
        recommender=TFIDFModel()
    )
    return vacancies


def main():
    uvicorn.run(
        "dreamjob.api.main:app",
        host="127.0.0.1",
        port=8080,
    )
