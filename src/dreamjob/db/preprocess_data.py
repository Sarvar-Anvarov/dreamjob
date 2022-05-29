import numpy as np

import re
from typing import List, Any
from pandas import DataFrame


def preprocess_data(vacancy_raw: DataFrame) -> DataFrame:
    """Preprocess raw vacancy data"""
    vacancy_df = (
        vacancy_raw
        .assign(
            key_skills=lambda df: df["key_skills"].apply(
                parse_multiple_values_cols
            ),
            specializations=lambda df: df["specializations"].apply(
                parse_multiple_values_cols
            ),
            professional_roles=lambda df: df["professional_roles"].apply(
                parse_multiple_values_cols, first_only=True
            ),
            description=lambda df: df["description"].apply(
                remove_tags
            ),
        )
    )

    return vacancy_df


def parse_multiple_values_cols(col: List, first_only: bool = False) -> Any:
    """Parse columns with multiple values and return List or its first value"""
    if first_only:
        return col[0]["name"] if len(col) > 0 else np.nan

    return [x["name"] for x in col]


def remove_tags(text: str) -> str:
    """Remove tags and quot from description"""
    tags = re.compile(r"<[^>]+>|&quot")

    return tags.sub("", text)
