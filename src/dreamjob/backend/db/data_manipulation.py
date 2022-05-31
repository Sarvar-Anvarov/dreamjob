import sqlalchemy
from io import StringIO

from dreamjob.backend.db.preprocess_data import array_literal
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
    """Update old vacancies info"""
    ...


def prepare_actual_vacancies():
    """Prepare actual vacancies for recommendations"""
    ...


def prepare_train_data():
    """Prepare train data to fit model"""
    ...
