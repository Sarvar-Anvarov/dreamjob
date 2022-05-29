import pandas as pd
import requests
import json

from typing import Tuple
from pandas import DataFrame

from dreamjob.config import settings
from structlog import get_logger

DISPLAY_COLS = settings.COLS
logger = get_logger()


def get_page(params: dict) -> Tuple[DataFrame, int, int]:
    """Get vacancy urls from a single page

    Args:
        params: parameters for hh.ru data request

    Returns:
        Dataframe with vacancies urls
        Max number of pages allowed (<=20)
        Number of found vacancies

    """
    response = requests.get('https://api.hh.ru/vacancies', params)
    json_file = json.loads(response.text)

    return pd.DataFrame(json_file["items"]), json_file["pages"], json_file["found"]


def get_pages(params: dict) -> DataFrame:
    """Get vacancy urls from several pages

    Args:
        params: parameters for hh.ru data request

    Returns:
        Dataframe with vacancies urls

    """
    vacancies_urls = pd.DataFrame()

    for page in range(20):
        params["page"] = page

        page_info, max_pages, vacancies_found = get_page(params)
        vacancies_urls = pd.concat([vacancies_urls, page_info])

        if max_pages - page <= 1:
            break

    logger.info("Pages are loaded",
                max_pages=max_pages,
                vacancies_found=vacancies_found,
                vacancies_allowed=min(2000, vacancies_found))

    return vacancies_urls[["id", "url"]]


def get_vacancies(area: int,
                  period: int,
                  per_page: int) -> DataFrame:
    """Get full vacancy descriptions

    Args:
        area: id of area (city, country, etc)
        period: number of days to include when requesting data
        per_page: number of vacancies per page (<=100)

    Returns:
        Dataframe with full vacancy descriptions

    """
    params = {
        "area": area,  # Saint-Petersburg id: 2
        "period": period,
        "per_page": per_page,
    }

    vacancies_urls = get_pages(params)
    vacancies_df = pd.DataFrame()

    for ind, url in enumerate(vacancies_urls["url"]):
        response = requests.get(url)
        json_file = json.loads(response.text)

        vacancies_info = pd.json_normalize(json_file)
        vacancies_df = pd.concat([vacancies_df, vacancies_info], ignore_index=True)

        if ind % 100 == 0:
            logger.info(f"Loading vacancy #{ind}")

    logger.info("Vacancies are loaded",
                vacancies_loaded=vacancies_df.shape[0])

    return vacancies_df[DISPLAY_COLS]
