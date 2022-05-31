import uvicorn
from fastapi import HTTPException
from fastapi import FastAPI

from dreamjob.backend.db.api import add_new_vacancies
from dreamjob.backend.db.create_db import create_db, create_table
from dreamjob.backend.config.logging_setup import setup_logging
from dreamjob.backend.config import settings


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


@app.get("/add_new_vacancies")
def add_new_vacancies_event(area: int = 2,
                            period: int = 1,
                            per_page: int = 100):
    try:
        add_new_vacancies(
            area=area, period=period, per_page=per_page
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "new vacancies were added"}


def main():
    uvicorn.run(
        "dreamjob.backend.api.main:app",
        host="127.0.0.1",
        port=8080,
    )
