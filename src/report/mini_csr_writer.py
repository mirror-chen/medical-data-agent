from pathlib import Path
from typing import Union

import pandas as pd


def extract_table_value(
        table_df: pd.DataFrame,
        variable: str,
        group: str,
) -> str:
    """
    Extract one value from a wide-format TLF table.
    """
    matched_rows = table_df[table_df["Variable"] == variable]

    if matched_rows.empty:
        return "not available"

    if group not in table_df.columns:
        return "not available"

    return str(matched_rows.iloc[0][group])


def generate_mini_csr_report(
        table_one: pd.DataFrame,
        output_path: Union[str, Path],
        adsl_columns: list = None,
        primary_endpoint_table: pd.DataFrame = None,
        treatment_difference_table: pd.DataFrame = None,
        exploratory_ttest_table: pd.DataFrame = None,
        output_files: dict = None,
) -> str:
    """
    Generate a mini CSR-style report section based on Table 1.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if adsl_columns is None:
        adsl_columns = []

    included_variables = ", ".join(adsl_columns) if adsl_columns else "not available"

    if output_files is None:
        output_files = {}

    traceability_lines = []

    for label, path in output_files.items():
        traceability_lines.append(f"- {label}: `{path}`")

    traceability_text = "\n".join(traceability_lines)

    drug_n = extract_table_value(table_one, "N", "Drug A")
    placebo_n = extract_table_value(table_one, "N", "Placebo")
    overall_n = extract_table_value(table_one, "N", "Overall")

    drug_age = extract_table_value(table_one, "Age, mean (SD)", "Drug A")
    placebo_age = extract_table_value(table_one, "Age, mean (SD)", "Placebo")
    overall_age = extract_table_value(table_one, "Age, mean (SD)", "Overall")

    drug_baseline = extract_table_value(table_one, "Baseline SBP, mean (SD)", "Drug A")
    placebo_baseline = extract_table_value(table_one, "Baseline SBP, mean (SD)", "Placebo")
    overall_baseline = extract_table_value(table_one, "Baseline SBP, mean (SD)", "Overall")

    efficacy_section = ""
    statistical_addendum = ""

    if primary_endpoint_table is not None and treatment_difference_table is not None:
        drug_row = primary_endpoint_table[
            primary_endpoint_table["Group"] == "Drug A"
            ]
        placebo_row = primary_endpoint_table[
            primary_endpoint_table["Group"] == "Placebo"
            ]

        diff_row = treatment_difference_table.iloc[0]

        if not drug_row.empty and not placebo_row.empty:
            drug_mean_chg = drug_row.iloc[0]["Mean CHG"]
            placebo_mean_chg = placebo_row.iloc[0]["Mean CHG"]
            drug_mean_pchg = drug_row.iloc[0]["Mean PCHG"]
            placebo_mean_pchg = placebo_row.iloc[0]["Mean PCHG"]

            endpoint_name = diff_row["Endpoint"]
            mean_chg_difference = diff_row["Mean CHG Difference"]
            mean_pchg_difference = diff_row["Mean PCHG Difference"]

            efficacy_section = f"""
## 4. Primary Endpoint Descriptive Summary

The primary endpoint was defined as {endpoint_name}.

In this synthetic demo dataset, the Drug A group showed a mean change from baseline of {drug_mean_chg}, compared with {placebo_mean_chg} in the placebo group. The corresponding mean percentage change from baseline was {drug_mean_pchg}% in the Drug A group and {placebo_mean_pchg}% in the placebo group.

The descriptive mean difference in change from baseline was {mean_chg_difference}, and the descriptive mean difference in percentage change from baseline was {mean_pchg_difference} percentage points.

These results are descriptive only. No statistical inference was performed. The observed difference should not be interpreted as confirmatory evidence of treatment effectiveness because the dataset is synthetic and the sample size is very small.
"""

        if exploratory_ttest_table is not None:
            ttest_row = exploratory_ttest_table.iloc[0]

            analysis_type = ttest_row["Analysis Type"]
            mean_chg_difference = ttest_row["Mean CHG Difference"]
            ci_level = ttest_row["CI Level"]
            ci_lower = ttest_row["CI Lower"]
            ci_upper = ttest_row["CI Upper"]
            p_value = ttest_row["P Value"]

            statistical_addendum = f"""
## 5. Exploratory Statistical Addendum

An {analysis_type} was generated for demonstration purposes using change from baseline as the analysis variable.

The estimated mean difference in change from baseline was {mean_chg_difference}. The {ci_level} confidence interval was {ci_lower} to {ci_upper}. The exploratory p-value was {p_value}.

This analysis is exploratory only and should not be interpreted as confirmatory evidence of treatment effectiveness. The dataset is synthetic and includes a very small number of subjects.
"""

    report = f"""# Mini CSR-style Report Demo

## 1. Data Standardization Summary

The source dataset was processed through an automated data mapping workflow. Raw source columns were scanned using a metadata profiling step and mapped to an ADSL-like analysis dataset structure. The resulting analysis-ready dataset included the following confirmed variables: {included_variables}.

All generated mappings were stored in a JSON mapping configuration file to support traceability between the raw source data and the derived analysis dataset.

## 2. Analysis Population

The demo ADSL-like dataset included {overall_n} subjects overall. The Drug A group included {drug_n} subjects and the placebo group included {placebo_n} subjects.

## 3. Demographic and Baseline Characteristics

The mean age was {drug_age} in the Drug A group and {placebo_age} in the placebo group. Overall the mean age was {overall_age}.

Baseline systolic blood pressure was {drug_baseline} in the Drug A group and {placebo_baseline} in the placebo group. Overall baseline systolic blood pressure was {overall_baseline}.

{efficacy_section}
{statistical_addendum}

## 6. Interpretation

This mini report demonstrates the first end-to-end workflow from raw client-style data to a standardized analysis-ready dataset and a structured CSR-style narrative. The current output is descriptive only and should not be interpreted as evidence of treatment effectiveness or safety.

## 7. Traceability

The following outputs were generated during this workflow:

{traceability_text}

"""

    output_path.write_text(report, encoding="utf-8")

    return report
