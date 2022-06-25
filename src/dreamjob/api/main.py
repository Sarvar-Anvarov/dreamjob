import uvicorn
from fastapi import FastAPI

from dreamjob.db.utils.create_db import create_db, create_table
from dreamjob.ml.recommend import choose_vacancies
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


# TODO: fix here with basemodel
@app.get("/recommend/{request}")
def recommend(request: str):
    vacancies = choose_vacancies(request)
    return vacancies


def main():
    uvicorn.run(
        "dreamjob.api.main:app",
        host="127.0.0.1",
        port=8080,
    )
