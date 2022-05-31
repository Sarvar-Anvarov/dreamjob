import uvicorn
from fastapi import FastAPI

from dreamjob.backend.db.api import router
from dreamjob.backend.db.create_db import create_db, create_table
from dreamjob.backend.config.logging_setup import setup_logging
from dreamjob.backend.config import settings

LOG_DIR = settings.LOG_DIR

app = FastAPI()
app.include_router(router, prefix="/data", tags=["data"])


@app.get("/")
def read_root():
    return {"status": "ok"}


@app.on_event("startup")
def startup_events():
    setup_logging(LOG_DIR)
    create_db()
    create_table()


def main():
    uvicorn.run(
        "dreamjob.backend.api.main:app",
        host="127.0.0.1",
        port=8080,
    )
