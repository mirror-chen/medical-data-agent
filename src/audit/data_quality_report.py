from pathlib import Path
from typing import Union

import pandas as pd


def summarize_column_quality(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate column-level data quality summary.
    """
    rows = []

    for column in df.columns:
        series = df[column]

        rows.append(
            {
                "column_name": column,
                "dtype": str(series.dtype),
                "missing_count": int(series.isna().sum()),
                "missing_rate": round(float(series.isna().mean()), 4),
                "unique_count": int(series.nunique(dropna=True)),
            }
        )

    return pd.DataFrame(rows)


def check_duplicate_subjects(
        df: pd.DataFrame,
        subject_column: str = "SUBJID",
) -> dict:
    """
    Check whether subject IDs are duplicated.
    """
    if subject_column not in df.columns:
        return {
            "check_name": "duplicate_subject_id",
            "status": "not_applicable",
            "message": f"{subject_column} is not available in the dataset.",
            "duplicate_count": None,
        }

    duplicate_count = int(df[subject_column].duplicated().sum())

    if duplicate_count == 0:
        status = "pass"
        message = "No duplicated subject IDs were detected."
    else:
        status = "fail"
        message = f"{duplicate_count} duplicated subject IDs were detected."

    return {
        "check_name": "duplicate_subject_id",
        "status": status,
        "message": message,
        "duplicate_count": duplicate_count,
    }


def generate_data_quality_report(
        raw_df: pd.DataFrame,
        adsl_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Generate a simple data quality report for raw and ADSL-like datasets.
    """
    rows = []

    rows.append(
        {
            "section": "dataset_summary",
            "check_name": "raw_row_count",
            "status": "info",
            "value": len(raw_df),
            "message": "Number of rows in the raw source dataset.",
        }
    )

    rows.append(
        {
            "section": "dataset_summary",
            "check_name": "raw_column_count",
            "status": "info",
            "value": len(raw_df.columns),
            "message": "Number of columns in the raw source dataset.",
        }
    )

    rows.append(
        {
            "section": "dataset_summary",
            "check_name": "adsl_row_count",
            "status": "info",
            "value": len(adsl_df),
            "message": "Number of rows in the ADSL-like analysis dataset.",
        }
    )

    rows.append(
        {
            "section": "dataset_summary",
            "check_name": "adsl_column_count",
            "status": "info",
            "value": len(adsl_df.columns),
            "message": "Number of columns in the ADSL-like analysis dataset.",
        }
    )

    duplicate_check = check_duplicate_subjects(adsl_df)
    rows.append(
        {
            "section": "subject_integrity",
            "check_name": duplicate_check["check_name"],
            "status": duplicate_check["status"],
            "value": duplicate_check["duplicate_count"],
            "message": duplicate_check["message"],
        }
    )

    column_quality = summarize_column_quality(adsl_df)

    for _, row in column_quality.iterrows():
        missing_rate = row["missing_rate"]

        if missing_rate == 0:
            status = "pass"
        elif missing_rate <= 0.2:
            status = "warning"
        else:
            status = "fail"

        rows.append(
            {
                "section": "column_quality",
                "check_name": f"missing_rate_{row['column_name']}",
                "status": status,
                "value": missing_rate,
                "message": (
                    f"{row['column_name']} has "
                    f"{row['missing_count']} missing values "
                    f"out of {len(adsl_df)} records."
                ),
            }
        )

    return pd.DataFrame(rows)


def save_data_quality_report(
        report_df: pd.DataFrame,
        output_path: Union[str, Path],
) -> None:
    """
    Save data quality report as CSV.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    report_df.to_csv(output_path, index=False)
