from pathlib import Path
from typing import Union

import numpy as np
import pandas as pd
from scipy import stats


def welch_ttest_chg(
        adeff_df: pd.DataFrame,
        endpoint_config: dict,
) -> pd.DataFrame:
    """
    Perform exploratory Welch two-sample t-test for CHG.

    This function is for exploratory analysis only.
    It should not be interpreted as confirmatory evidence.
    """
    treatment_variable = endpoint_config["treatment_variable"]
    active_group = endpoint_config["active_group"]
    control_group = endpoint_config["control_group"]
    endpoint_name = endpoint_config["primary_endpoint_name"]
    alpha = float(endpoint_config.get("alpha", 0.05))

    required_columns = [treatment_variable, "CHG"]

    missing_columns = [
        column for column in required_columns
        if column not in adeff_df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Cannot run exploratory t-test. Missing columns: {missing_columns}"
        )

    active_values = pd.to_numeric(
        adeff_df.loc[adeff_df[treatment_variable] == active_group, "CHG"],
        errors="coerce",
    ).dropna()

    control_values = pd.to_numeric(
        adeff_df.loc[adeff_df[treatment_variable] == control_group, "CHG"],
        errors="coerce",
    ).dropna()

    if len(active_values) < 2 or len(control_values) < 2:
        raise ValueError(
            "Welch t-test requires at least two non-missing observations per group."
        )

    active_mean = float(active_values.mean())
    control_mean = float(control_values.mean())
    mean_difference = active_mean - control_mean

    active_var = float(active_values.var(ddof=1))
    control_var = float(control_values.var(ddof=1))

    active_n = int(len(active_values))
    control_n = int(len(control_values))

    standard_error = np.sqrt(
        (active_var / active_n) + (control_var / control_n)
    )

    numerator = ((active_var / active_n) + (control_var / control_n)) ** 2
    denominator = (
            ((active_var / active_n) ** 2) / (active_n - 1)
            + ((control_var / control_n) ** 2) / (control_n - 1)
    )

    degrees_of_freedom = numerator / denominator

    t_statistic, p_value = stats.ttest_ind(
        active_values,
        control_values,
        equal_var=False,
    )

    critical_value = stats.t.ppf(
        1 - alpha / 2,
        degrees_of_freedom,
        )

    ci_lower = mean_difference - critical_value * standard_error
    ci_upper = mean_difference + critical_value * standard_error

    result = {
        "Endpoint": endpoint_name,
        "Analysis Type": "Exploratory Welch two-sample t-test",
        "Active Group": active_group,
        "Control Group": control_group,
        "Active N": active_n,
        "Control N": control_n,
        "Active Mean CHG": round(active_mean, 2),
        "Control Mean CHG": round(control_mean, 2),
        "Mean CHG Difference": round(mean_difference, 2),
        "Standard Error": round(float(standard_error), 4),
        "Degrees of Freedom": round(float(degrees_of_freedom), 4),
        "T Statistic": round(float(t_statistic), 4),
        "P Value": round(float(p_value), 4),
        "CI Level": f"{int((1 - alpha) * 100)}%",
        "CI Lower": round(float(ci_lower), 2),
        "CI Upper": round(float(ci_upper), 2),
        "Interpretation Boundary": (
            "Exploratory only. Not confirmatory. "
            "The dataset is synthetic and the sample size is very small."
        ),
    }

    return pd.DataFrame([result])


def save_exploratory_ttest_table(
        table_df: pd.DataFrame,
        output_path: Union[str, Path],
) -> None:
    """
    Save exploratory t-test table as CSV.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    table_df.to_csv(output_path, index=False)
