from pathlib import Path
from typing import Union

import pandas as pd


def calculate_treatment_difference(
        adeff_df: pd.DataFrame,
        endpoint_config: dict,
) -> pd.DataFrame:
    """
    Calculate descriptive treatment difference for a continuous endpoint.

    Current prototype compares mean CHG between active and control groups.
    This is descriptive only and does not perform confirmatory inference.
    """
    treatment_variable = endpoint_config["treatment_variable"]
    active_group = endpoint_config["active_group"]
    control_group = endpoint_config["control_group"]
    endpoint_name = endpoint_config["primary_endpoint_name"]

    required_columns = [
        treatment_variable,
        "CHG",
        "PCHG",
    ]

    missing_columns = [
        column for column in required_columns
        if column not in adeff_df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Cannot calculate treatment difference. Missing columns: {missing_columns}"
        )

    active_df = adeff_df[adeff_df[treatment_variable] == active_group]
    control_df = adeff_df[adeff_df[treatment_variable] == control_group]

    if active_df.empty:
        raise ValueError(f"Active group not found: {active_group}")

    if control_df.empty:
        raise ValueError(f"Control group not found: {control_group}")

    active_chg = pd.to_numeric(active_df["CHG"], errors="coerce")
    control_chg = pd.to_numeric(control_df["CHG"], errors="coerce")

    active_pchg = pd.to_numeric(active_df["PCHG"], errors="coerce")
    control_pchg = pd.to_numeric(control_df["PCHG"], errors="coerce")

    active_mean_chg = float(active_chg.mean())
    control_mean_chg = float(control_chg.mean())

    active_mean_pchg = float(active_pchg.mean())
    control_mean_pchg = float(control_pchg.mean())

    mean_chg_difference = active_mean_chg - control_mean_chg
    mean_pchg_difference = active_mean_pchg - control_mean_pchg

    result = {
        "Endpoint": endpoint_name,
        "Active Group": active_group,
        "Control Group": control_group,
        "Active N": int(active_chg.notna().sum()),
        "Control N": int(control_chg.notna().sum()),
        "Active Mean CHG": round(active_mean_chg, 2),
        "Control Mean CHG": round(control_mean_chg, 2),
        "Mean CHG Difference": round(mean_chg_difference, 2),
        "Active Mean PCHG": round(active_mean_pchg, 2),
        "Control Mean PCHG": round(control_mean_pchg, 2),
        "Mean PCHG Difference": round(mean_pchg_difference, 2),
        "Analysis Type": "Descriptive treatment difference",
        "Interpretation Boundary": (
            "Descriptive only. Not confirmatory. No statistical inference was performed."
        ),
    }

    return pd.DataFrame([result])


def save_treatment_difference_table(
        table_df: pd.DataFrame,
        output_path: Union[str, Path],
) -> None:
    """
    Save treatment difference table as CSV.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    table_df.to_csv(output_path, index=False)
