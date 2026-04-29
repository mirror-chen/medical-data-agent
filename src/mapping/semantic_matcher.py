from typing import Any


TARGET_VARIABLE_DICTIONARY = {
    "SUBJID": {
        "keywords": ["subject", "subject_no", "subject_id", "subjid", "patient", "patient_id", "pt_id"],
        "description": "Subject identifier",
    },
    "USUBJID": {
        "keywords": ["usubjid", "unique_subject", "unique_subject_id"],
        "description": "Unique subject identifier",
    },
    "SEX": {
        "keywords": ["sex", "gender", "pt_gender", "biological_sex"],
        "description": "Sex or gender variable",
    },
    "AGE": {
        "keywords": ["age", "patient_age", "subject_age"],
        "description": "Age at baseline or enrollment",
    },
    "TRT01P": {
        "keywords": ["treatment", "treatment_group", "arm", "group", "trt", "planned_treatment"],
        "description": "Planned treatment group",
    },
    "TRT01A": {
        "keywords": ["actual_treatment", "actual_trt", "treatment_actual"],
        "description": "Actual treatment group",
    },
    "BASELINE": {
        "keywords": ["baseline", "baseline_value", "baseline_sbp", "base"],
        "description": "Baseline measurement",
    },
    "AVAL": {
        "keywords": ["followup", "followup_value", "post_baseline", "endpoint", "outcome", "aval"],
        "description": "Analysis value or post-baseline outcome",
    },
}


def normalize_column_name(column_name: str) -> str:
    """
    Normalize raw column names for matching.
    """
    return (
        column_name.strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace(".", "_")
    )


def calculate_keyword_score(normalized_column: str, keywords: list[str]) -> float:
    """
    Calculate a simple rule-based confidence score by keyword matching.
    """
    if normalized_column in keywords:
        return 0.95

    for keyword in keywords:
        if keyword in normalized_column:
            return 0.85

    for keyword in keywords:
        keyword_parts = keyword.split("_")
        if all(part in normalized_column for part in keyword_parts):
            return 0.75

    return 0.0


def infer_target_variable(column_profile: dict[str, Any]) -> dict[str, Any]:
    """
    Infer the most likely target variable for one raw column.
    """
    column_name = column_profile["column_name"]
    normalized_column = normalize_column_name(column_name)

    best_target = None
    best_score = 0.0
    best_reason = "No matching rule was found."

    for target_variable, target_info in TARGET_VARIABLE_DICTIONARY.items():
        score = calculate_keyword_score(
            normalized_column,
            target_info["keywords"],
        )

        if score > best_score:
            best_target = target_variable
            best_score = score
            best_reason = (
                f"Column name '{column_name}' matched keywords for "
                f"{target_variable}: {target_info['keywords']}"
            )

    if best_score >= 0.90:
        review_status = "auto_accept_candidate"
        needs_review = False
    elif best_score >= 0.75:
        review_status = "review_recommended"
        needs_review = True
    elif best_score >= 0.50:
        review_status = "manual_review_required"
        needs_review = True
    else:
        review_status = "unmapped"
        needs_review = True

    return {
        "source_column": column_name,
        "target_variable": best_target,
        "confidence": round(best_score, 2),
        "review_status": review_status,
        "needs_review": needs_review,
        "reason": best_reason,
    }


def generate_mapping_draft(metadata: dict[str, Any]) -> dict[str, Any]:
    """
    Generate a mapping draft from metadata scanner output.
    """
    mappings = []

    for column_profile in metadata["columns"]:
        mapping = infer_target_variable(column_profile)
        mappings.append(mapping)

    return {
        "source_file": metadata["file_name"],
        "n_columns": metadata["n_columns"],
        "mappings": mappings,
    }
