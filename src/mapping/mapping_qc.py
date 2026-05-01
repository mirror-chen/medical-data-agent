from pathlib import Path
from typing import Union

import pandas as pd


def assign_mapping_risk_level(mapping: dict) -> str:
    """
    Assign a simple QC risk level to one mapping.
    """
    confidence = mapping.get("confidence", 0.0)
    human_decision = mapping.get("human_decision", "pending")
    target_variable = mapping.get("target_variable")

    if target_variable is None:
        return "High"

    if human_decision == "unmapped":
        return "High"

    if human_decision == "pending_review":
        return "High"

    if human_decision == "manually_accepted":
        return "Medium"

    if human_decision == "auto_accepted" and confidence >= 0.90:
        return "Low"

    return "Medium"


def generate_qc_message(mapping: dict) -> str:
    """
    Generate a human-readable QC message for one mapping.
    """
    source_column = mapping.get("source_column")
    target_variable = mapping.get("target_variable")
    confidence = mapping.get("confidence", 0.0)
    human_decision = mapping.get("human_decision", "pending")

    if target_variable is None:
        return f"{source_column} was not mapped to any target variable."

    if human_decision == "auto_accepted":
        return (
            f"{source_column} was automatically mapped to {target_variable} "
            f"with confidence {confidence}."
        )

    if human_decision == "manually_accepted":
        return (
            f"{source_column} was manually confirmed as {target_variable} "
            f"after review."
        )

    if human_decision == "pending_review":
        return (
            f"{source_column} was suggested as {target_variable} "
            f"but still requires human review."
        )

    return f"{source_column} mapping status requires additional QC review."


def generate_mapping_qc_report(mapping_config: dict) -> pd.DataFrame:
    """
    Generate a QC report for mapping decisions.
    """
    rows = []

    for mapping in mapping_config["mappings"]:
        rows.append(
            {
                "source_column": mapping.get("source_column"),
                "target_variable": mapping.get("target_variable"),
                "confidence": mapping.get("confidence"),
                "human_confirmed": mapping.get("human_confirmed"),
                "human_decision": mapping.get("human_decision"),
                "review_status": mapping.get("review_status"),
                "risk_level": assign_mapping_risk_level(mapping),
                "qc_message": generate_qc_message(mapping),
            }
        )

    return pd.DataFrame(rows)


def save_mapping_qc_report(
        qc_report: pd.DataFrame,
        output_path: Union[str, Path],
) -> None:
    """
    Save mapping QC report as CSV.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    qc_report.to_csv(output_path, index=False)
