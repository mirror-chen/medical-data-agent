from pathlib import Path
from typing import Union

import pandas as pd


def _format_count_percent(count: int, denominator: int) -> str:
    """
    Format count and percentage for safety tables.
    """
    if denominator == 0:
        return "0 (0.0%)"

    percent = round((count / denominator) * 100, 1)
    return f"{count} ({percent}%)"


def _count_subjects_with_condition(
        adae_df: pd.DataFrame,
        condition: pd.Series,
) -> int:
    """
    Count unique subjects meeting a safety condition.
    """
    return int(adae_df.loc[condition, "SUBJID"].nunique())


def create_safety_summary_table(
        adae_df: pd.DataFrame,
        adsl_df: pd.DataFrame,
        treatment_column: str = "TRT01P",
) -> pd.DataFrame:
    """
    Create a subject-level safety summary table.

    Percentages are based on subjects in the ADSL-like dataset by treatment group.
    """
    treatment_groups = sorted(
        adsl_df[treatment_column].dropna().unique().tolist()
    )
    groups = treatment_groups + ["Overall"]

    rows = []

    for group in groups:
        if group == "Overall":
            group_adsl = adsl_df
            group_adae = adae_df
        else:
            group_adsl = adsl_df[adsl_df[treatment_column] == group]
            group_adae = adae_df[adae_df[treatment_column] == group]

        denominator = int(group_adsl["SUBJID"].nunique())

        teae_condition = group_adae["TRTEMFL"] == "Y"
        sae_condition = teae_condition & (group_adae["AESER"] == "Y")
        severe_condition = teae_condition & (group_adae["AESEV"] == "SEVERE")
        related_condition = teae_condition & (group_adae["AEREL"] == "Y")

        rows.extend(
            [
                {
                    "Safety Category": "Subjects in safety population",
                    "Group": group,
                    "Value": str(denominator),
                },
                {
                    "Safety Category": "Subjects with any TEAE",
                    "Group": group,
                    "Value": _format_count_percent(
                        _count_subjects_with_condition(
                            group_adae,
                            teae_condition,
                        ),
                        denominator,
                    ),
                },
                {
                    "Safety Category": "Subjects with any SAE",
                    "Group": group,
                    "Value": _format_count_percent(
                        _count_subjects_with_condition(
                            group_adae,
                            sae_condition,
                        ),
                        denominator,
                    ),
                },
                {
                    "Safety Category": "Subjects with severe TEAE",
                    "Group": group,
                    "Value": _format_count_percent(
                        _count_subjects_with_condition(
                            group_adae,
                            severe_condition,
                        ),
                        denominator,
                    ),
                },
                {
                    "Safety Category": "Subjects with related TEAE",
                    "Group": group,
                    "Value": _format_count_percent(
                        _count_subjects_with_condition(
                            group_adae,
                            related_condition,
                        ),
                        denominator,
                    ),
                },
                {
                    "Safety Category": "Total TEAE events",
                    "Group": group,
                    "Value": str(int(teae_condition.sum())),
                },
            ]
        )

    long_table = pd.DataFrame(rows)

    wide_table = long_table.pivot(
        index="Safety Category",
        columns="Group",
        values="Value",
    ).reset_index()

    preferred_order = ["Safety Category", "Drug A", "Placebo", "Overall"]
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


def save_safety_summary_table(
        table_df: pd.DataFrame,
        output_path: Union[str, Path],
) -> None:
    """
    Save safety summary table as CSV.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    table_df.to_csv(output_path, index=False)
