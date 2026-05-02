from pathlib import Path
from typing import Union

import pandas as pd

from src.mapping.metadata_scanner import load_raw_data


def build_adae_like_dataset(
        raw_ae_data_path: Union[str, Path],
        adsl_df: pd.DataFrame,
        safety_config: dict,
) -> pd.DataFrame:
    """
    Build an ADAE-like safety analysis dataset from raw AE data.

    Current prototype supports basic AE standardization and TEAE derivation.
    """
    raw_ae_df = load_raw_data(raw_ae_data_path)

    required_columns = [
        "Subject_No",
        "Treatment_Group",
        "AE_Term",
        "AE_Start_Day",
        "AE_End_Day",
        "AE_Severity",
        "AE_Serious",
        "AE_Related",
    ]

    missing_columns = [
        column for column in required_columns
        if column not in raw_ae_df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Cannot build ADAE-like dataset. Missing columns: {missing_columns}"
        )

    adae_df = pd.DataFrame()

    adae_df["SUBJID"] = raw_ae_df["Subject_No"].astype(str)
    adae_df["TRT01P"] = raw_ae_df["Treatment_Group"].astype(str)
    adae_df["AETERM"] = raw_ae_df["AE_Term"].astype(str)

    adae_df["ASTDY"] = pd.to_numeric(
        raw_ae_df["AE_Start_Day"],
        errors="coerce",
    )

    adae_df["AENDY"] = pd.to_numeric(
        raw_ae_df["AE_End_Day"],
        errors="coerce",
    )

    adae_df["AESEV"] = (
        raw_ae_df["AE_Severity"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    adae_df["AESER"] = (
        raw_ae_df["AE_Serious"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    adae_df["AEREL"] = (
        raw_ae_df["AE_Related"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    treatment_start_day = int(
        safety_config.get("treatment_start_day", 1)
    )

    adae_df["TRTEMFL"] = adae_df["ASTDY"].apply(
        lambda value: "Y"
        if pd.notna(value) and value >= treatment_start_day
        else "N"
    )

    safety_subjects = adsl_df[["SUBJID", "TRT01P"]].drop_duplicates()

    adae_df = adae_df.merge(
        safety_subjects,
        on=["SUBJID", "TRT01P"],
        how="inner",
    )

    return adae_df


def save_adae_like_dataset(
        adae_df: pd.DataFrame,
        output_path: Union[str, Path],
) -> None:
    """
    Save ADAE-like dataset as CSV.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    adae_df.to_csv(output_path, index=False)
