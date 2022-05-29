import uvicorn
from fastapi import HTTPException

from dreamjob.db.api import add_new_vacancies
from dreamjob.db.create_db import create_db, create_table
from dreamjob.config.logging_setup import setup_logging
from dreamjob.config import settings

from typing import Union
from fastapi import FastAPI

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


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


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

    return {"post status": "new vacancies were added"}


def main():
    uvicorn.run(
        "dreamjob.api.main:app",
        host="127.0.0.1",
        port=8080,
    )
