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
) -> str:
    """
    Generate a mini CSR-style report section based on Table 1.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if adsl_columns is None:
        adsl_columns = []

    included_variables = ", ".join(adsl_columns) if adsl_columns else "not available"

    drug_n = extract_table_value(table_one, "N", "Drug A")
    placebo_n = extract_table_value(table_one, "N", "Placebo")
    overall_n = extract_table_value(table_one, "N", "Overall")

    drug_age = extract_table_value(table_one, "Age, mean (SD)", "Drug A")
    placebo_age = extract_table_value(table_one, "Age, mean (SD)", "Placebo")
    overall_age = extract_table_value(table_one, "Age, mean (SD)", "Overall")

    drug_baseline = extract_table_value(table_one, "Baseline SBP, mean (SD)", "Drug A")
    placebo_baseline = extract_table_value(table_one, "Baseline SBP, mean (SD)", "Placebo")
    overall_baseline = extract_table_value(table_one, "Baseline SBP, mean (SD)", "Overall")

    report = f"""# Mini CSR-style Report Demo

## 1. Data Standardization Summary

The source dataset was processed through an automated data mapping workflow. Raw source columns were scanned using a metadata profiling step and mapped to an ADSL-like analysis dataset structure. The resulting analysis-ready dataset included the following confirmed variables: {included_variables}.
All generated mappings were stored in a JSON mapping configuration file to support traceability between the raw source data and the derived analysis dataset.

## 2. Analysis Population

The demo ADSL-like dataset included {overall_n} subjects overall. The Drug A group included {drug_n} subjects and the placebo group included {placebo_n} subjects.

## 3. Demographic and Baseline Characteristics

The mean age was {drug_age} in the Drug A group and {placebo_age} in the placebo group. Overall the mean age was {overall_age}.

Baseline systolic blood pressure was {drug_baseline} in the Drug A group and {placebo_baseline} in the placebo group. Overall baseline systolic blood pressure was {overall_baseline}.

## 4. Interpretation

This mini report demonstrates the first end-to-end workflow from raw client-style data to a standardized analysis-ready dataset and a structured CSR-style narrative. The current output is descriptive only and should not be interpreted as evidence of treatment effectiveness or safety.

## 5. Traceability

The following outputs were generated during this workflow:

- Mapping configuration: `outputs/audit_logs/mapping_config_demo.json`
- ADSL-like dataset: `data/adam_like/adsl_demo.csv`
- Table 1: `outputs/tables/table_one_demo.csv`

"""

    output_path.write_text(report, encoding="utf-8")

    return report
