from pathlib import Path
from typing import Union

import pandas as pd


def summarize_continuous(
        df: pd.DataFrame,
        variable: str,
) -> dict:
    """
    Summarize a continuous variable.
    """
    values = pd.to_numeric(df[variable], errors="coerce")

    return {
        "n": int(values.notna().sum()),
        "mean": round(float(values.mean()), 2),
        "sd": round(float(values.std()), 2),
        "median": round(float(values.median()), 2),
        "min": round(float(values.min()), 2),
        "max": round(float(values.max()), 2),
    }


def summarize_categorical(
        df: pd.DataFrame,
        variable: str,
) -> dict:
    """
    Summarize a categorical variable.
    """
    total = len(df)
    counts = df[variable].fillna("Missing").value_counts(dropna=False)

    summary = {}

    for category, count in counts.items():
        percent = round((count / total) * 100, 1) if total > 0 else 0
        summary[str(category)] = {
            "n": int(count),
            "percent": percent,
        }

    return summary


def create_demographics_baseline_table(
        adsl_df: pd.DataFrame,
        treatment_column: str = "TRT01P",
) -> pd.DataFrame:
    """
    Create a simple demographics and baseline characteristics table.
    """
    treatment_groups = sorted(adsl_df[treatment_column].dropna().unique().tolist())
    groups = treatment_groups + ["Overall"]

    rows = []

    for group in groups:
        if group == "Overall":
            group_df = adsl_df
        else:
            group_df = adsl_df[adsl_df[treatment_column] == group]

        n_subjects = len(group_df)

        rows.append({
            "Variable": "N",
            "Group": group,
            "Value": str(n_subjects),
        })

        if "AGE" in group_df.columns:
            age_summary = summarize_continuous(group_df, "AGE")
            rows.append({
                "Variable": "Age, mean (SD)",
                "Group": group,
                "Value": f"{age_summary['mean']} ({age_summary['sd']})",
            })
            rows.append({
                "Variable": "Age, median (min, max)",
                "Group": group,
                "Value": (
                    f"{age_summary['median']} "
                    f"({age_summary['min']}, {age_summary['max']})"
                ),
            })

        if "SEX" in group_df.columns:
            sex_summary = summarize_categorical(group_df, "SEX")
            for sex_category, sex_values in sex_summary.items():
                rows.append({
                    "Variable": f"Sex, {sex_category}, n (%)",
                    "Group": group,
                    "Value": f"{sex_values['n']} ({sex_values['percent']}%)",
                })

        if "BASELINE" in group_df.columns:
            baseline_summary = summarize_continuous(group_df, "BASELINE")
            rows.append({
                "Variable": "Baseline SBP, mean (SD)",
                "Group": group,
                "Value": (
                    f"{baseline_summary['mean']} "
                    f"({baseline_summary['sd']})"
                ),
            })

    long_table = pd.DataFrame(rows)

    wide_table = long_table.pivot(
        index="Variable",
        columns="Group",
        values="Value",
    ).reset_index()

    wide_table = wide_table.fillna("0 (0.0%)")

    preferred_order = ["Variable", "Drug A", "Placebo", "Overall"]
    available_order = [
        column for column in preferred_order
        if column in wide_table.columns
    ]

    remaining_columns = [
        column for column in wide_table.columns
        if column not in available_order
    ]

    wide_table = wide_table[available_order + remaining_columns]

    return wide_table


def save_table(
        table_df: pd.DataFrame,
        output_path: Union[str, Path],
) -> None:
    """
    Save TLF table as CSV.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    table_df.to_csv(output_path, index=False)
