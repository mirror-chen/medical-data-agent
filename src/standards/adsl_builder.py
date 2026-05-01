from pathlib import Path
from typing import Union

import pandas as pd

from src.mapping.metadata_scanner import load_raw_data
from src.mapping.mapping_config_manager import load_mapping_config
from src.mapping.value_mapper import standardize_adsl_values


def build_adsl_like_dataset(
        raw_data_path: Union[str, Path],
        mapping_config_path: Union[str, Path],
) -> pd.DataFrame:
    """
    Build an ADSL-like analysis dataset from raw data and a mapping config.

    This function uses confirmed or high-confidence mappings to rename raw
    columns into target analysis variables.
    """
    raw_df = load_raw_data(raw_data_path)
    mapping_config = load_mapping_config(mapping_config_path)

    rename_map = {}

    for mapping in mapping_config["mappings"]:
        source_column = mapping["source_column"]
        target_variable = mapping["target_variable"]
        human_confirmed = mapping.get("human_confirmed", False)

        if target_variable is None:
            continue

        if not human_confirmed:
            continue

        if source_column in raw_df.columns:
            rename_map[source_column] = target_variable

    adsl_df = raw_df.rename(columns=rename_map)

    selected_columns = [
        "SUBJID",
        "SEX",
        "AGE",
        "TRT01P",
        "BASELINE",
        "AVAL",
    ]

    available_columns = [
        column for column in selected_columns
        if column in adsl_df.columns
    ]

    adsl_df = adsl_df[available_columns]
    adsl_df = standardize_adsl_values(adsl_df)

    return adsl_df


def save_adsl_like_dataset(
        adsl_df: pd.DataFrame,
        output_path: Union[str, Path],
) -> None:
    """
    Save the ADSL-like dataset as CSV.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    adsl_df.to_csv(output_path, index=False)
