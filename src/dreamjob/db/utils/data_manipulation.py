import pandas as pd
import sqlalchemy
from io import StringIO

from .preprocess_data import array_literal
from pandas import DataFrame


def insert(vacancies: DataFrame, engine: sqlalchemy.engine.base.Engine):
    """Insert new vacancies into table"""
    vacancies = (
        vacancies
        .assign(
            **{
                "key_skills": lambda df: df["key_skills"].apply(array_literal),
                "specializations": lambda df: df["specializations"].apply(array_literal),
            }
        )
    )

    raw_con = engine.raw_connection()

    with raw_con.cursor() as cursor:
        buffer = StringIO()
        vacancies.to_csv(buffer, sep='\t', header=False, index=False)

        buffer.seek(0)
        cursor.copy_from(buffer, "vacancies", null="")
        raw_con.commit()

    return vacancies.shape[0]


def update():
    """Update old vacancies"""
    ...


def select(engine: sqlalchemy.engine.base.Engine,
           columns: str = "*", top_n: int = 0, top_query: str = "") -> DataFrame:
    """Select vacancies"""
    if top_n:
        top_query = f"LIMIT {top_n}"

    return pd.read_sql_query(
        f"""
        SELECT {columns} FROM vacancies {top_query}
        """,
        con=engine
    )

