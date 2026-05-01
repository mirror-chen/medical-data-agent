from pathlib import Path
from typing import Union

import pandas as pd


def summarize_endpoint_by_group(
        adeff_df: pd.DataFrame,
        treatment_column: str = "TRT01P",
) -> pd.DataFrame:
    """
    Generate a primary endpoint summary table by treatment group.

    Current prototype summarizes continuous change-from-baseline endpoints.
    """
    required_columns = [treatment_column, "CHG", "PCHG"]

    missing_columns = [
        column for column in required_columns
        if column not in adeff_df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Cannot summarize endpoint. Missing columns: {missing_columns}"
        )

    rows = []

    treatment_groups = sorted(
        adeff_df[treatment_column].dropna().unique().tolist()
    )

    for group in treatment_groups:
        group_df = adeff_df[adeff_df[treatment_column] == group]

        chg_values = pd.to_numeric(group_df["CHG"], errors="coerce")
        pchg_values = pd.to_numeric(group_df["PCHG"], errors="coerce")

        rows.append(
            {
                "Group": group,
                "N": int(chg_values.notna().sum()),
                "Mean CHG": round(float(chg_values.mean()), 2),
                "SD CHG": round(float(chg_values.std()), 2),
                "Median CHG": round(float(chg_values.median()), 2),
                "Min CHG": round(float(chg_values.min()), 2),
                "Max CHG": round(float(chg_values.max()), 2),
                "Mean PCHG": round(float(pchg_values.mean()), 2),
                "SD PCHG": round(float(pchg_values.std()), 2),
            }
        )

    overall_chg = pd.to_numeric(adeff_df["CHG"], errors="coerce")
    overall_pchg = pd.to_numeric(adeff_df["PCHG"], errors="coerce")

    rows.append(
        {
            "Group": "Overall",
            "N": int(overall_chg.notna().sum()),
            "Mean CHG": round(float(overall_chg.mean()), 2),
            "SD CHG": round(float(overall_chg.std()), 2),
            "Median CHG": round(float(overall_chg.median()), 2),
            "Min CHG": round(float(overall_chg.min()), 2),
            "Max CHG": round(float(overall_chg.max()), 2),
            "Mean PCHG": round(float(overall_pchg.mean()), 2),
            "SD PCHG": round(float(overall_pchg.std()), 2),
        }
    )

    return pd.DataFrame(rows)


def save_primary_endpoint_table(
        table_df: pd.DataFrame,
        output_path: Union[str, Path],
) -> None:
    """
    Save primary endpoint summary table as CSV.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    table_df.to_csv(output_path, index=False)
