from pathlib import Path
from typing import Union

import pandas as pd


def build_adeff_like_dataset(
        adsl_df: pd.DataFrame,
        endpoint_config: dict,
) -> pd.DataFrame:
    """
    Build an ADEFF-like efficacy analysis dataset from ADSL-like data.

    Current prototype supports a continuous change-from-baseline endpoint.
    """
    baseline_variable = endpoint_config["baseline_variable"]
    analysis_variable = endpoint_config["analysis_variable"]
    treatment_variable = endpoint_config["treatment_variable"]
    primary_endpoint_name = endpoint_config["primary_endpoint_name"]

    required_columns = [
        "SUBJID",
        treatment_variable,
        baseline_variable,
        analysis_variable,
    ]

    missing_columns = [
        column for column in required_columns
        if column not in adsl_df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Cannot build ADEFF-like dataset. Missing columns: {missing_columns}"
        )

    adeff_df = pd.DataFrame()

    adeff_df["SUBJID"] = adsl_df["SUBJID"]
    adeff_df["TRT01P"] = adsl_df[treatment_variable]
    adeff_df["PARAM"] = primary_endpoint_name

    adeff_df["BASE"] = pd.to_numeric(
        adsl_df[baseline_variable],
        errors="coerce",
    )

    adeff_df["AVAL"] = pd.to_numeric(
        adsl_df[analysis_variable],
        errors="coerce",
    )

    adeff_df["CHG"] = adeff_df["AVAL"] - adeff_df["BASE"]

    adeff_df["PCHG"] = (
                               adeff_df["CHG"] / adeff_df["BASE"]
                       ) * 100

    adeff_df["PCHG"] = adeff_df["PCHG"].round(2)

    return adeff_df


def save_adeff_like_dataset(
        adeff_df: pd.DataFrame,
        output_path: Union[str, Path],
) -> None:
    """
    Save ADEFF-like dataset as CSV.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    adeff_df.to_csv(output_path, index=False)
