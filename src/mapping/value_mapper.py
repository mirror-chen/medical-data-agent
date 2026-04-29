from typing import Dict

import pandas as pd


STANDARD_VALUE_MAPS = {
    "SEX": {
        "1": "M",
        "2": "F",
        "male": "M",
        "female": "F",
        "m": "M",
        "f": "F",
    },
    "YES_NO": {
        "1": "Y",
        "0": "N",
        "yes": "Y",
        "no": "N",
        "y": "Y",
        "n": "N",
    },
    "SEVERITY": {
        "mild": "MILD",
        "moderate": "MODERATE",
        "severe": "SEVERE",
    },
}


def apply_value_mapping(
        df: pd.DataFrame,
        target_variable: str,
        value_map: Dict[str, str],
) -> pd.DataFrame:
    """
    Apply standardized value mapping to a target variable.
    """
    df = df.copy()

    if target_variable not in df.columns:
        return df

    df[target_variable] = (
        df[target_variable]
        .astype(str)
        .str.strip()
        .str.lower()
        .map(value_map)
        .fillna(df[target_variable])
    )

    return df


def standardize_adsl_values(adsl_df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply standard value mappings to ADSL-like dataset.
    """
    adsl_df = adsl_df.copy()

    if "SEX" in adsl_df.columns:
        adsl_df = apply_value_mapping(
            adsl_df,
            target_variable="SEX",
            value_map=STANDARD_VALUE_MAPS["SEX"],
        )

    return adsl_df
