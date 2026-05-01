from typing import List, Dict, Any


def auto_confirm_high_confidence_mappings(
        mapping_draft: dict,
        auto_accept_threshold: float = 0.90,
) -> dict:
    """
    Auto-confirm high-confidence mappings.

    This simulates the first version of human-in-the-loop logic.
    High-confidence mappings can be auto-accepted as candidates.
    Lower-confidence mappings remain pending for review.
    """
    reviewed_mappings: List[Dict[str, Any]] = []

    for mapping in mapping_draft["mappings"]:
        mapping = mapping.copy()

        confidence = mapping.get("confidence", 0.0)
        target_variable = mapping.get("target_variable")

        if target_variable is None:
            mapping["human_confirmed"] = False
            mapping["human_decision"] = "unmapped"
            mapping["review_status"] = "manual_review_required"

        elif confidence >= auto_accept_threshold:
            mapping["human_confirmed"] = True
            mapping["human_decision"] = "auto_accepted"
            mapping["review_status"] = "auto_accepted"

        else:
            mapping["human_confirmed"] = False
            mapping["human_decision"] = "pending_review"
            mapping["review_status"] = "review_required"

        reviewed_mappings.append(mapping)

    reviewed_config = mapping_draft.copy()
    reviewed_config["mappings"] = reviewed_mappings
    reviewed_config["review_policy"] = {
        "auto_accept_threshold": auto_accept_threshold,
        "rule": "Mappings with confidence >= threshold are auto-confirmed. Others require human review.",
    }

    return reviewed_config


def summarize_review_status(mapping_config: dict) -> dict:
    """
    Summarize mapping review status.
    """
    summary = {
        "total_mappings": 0,
        "auto_accepted": 0,
        "manually_accepted": 0,
        "pending_review": 0,
        "manual_review_required": 0,
        "unmapped": 0,
    }

    for mapping in mapping_config["mappings"]:
        summary["total_mappings"] += 1

        decision = mapping.get("human_decision")

        if decision == "auto_accepted":
            summary["auto_accepted"] += 1
        elif decision == "manually_accepted":
            summary["manually_accepted"] += 1
        elif decision == "pending_review":
            summary["pending_review"] += 1
        elif decision == "unmapped":
            summary["unmapped"] += 1
        else:
            summary["manual_review_required"] += 1

    return summary


def apply_manual_overrides(
        mapping_config: dict,
        manual_overrides: dict,
) -> dict:
    """
    Apply manual review decisions to a mapping configuration.

    manual_overrides format:
    {
        "Followup_SBP": {
            "target_variable": "AVAL",
            "human_decision": "manually_accepted"
        }
    }
    """
    updated_config = mapping_config.copy()
    updated_mappings = []

    for mapping in updated_config["mappings"]:
        mapping = mapping.copy()
        source_column = mapping["source_column"]

        if source_column in manual_overrides:
            override = manual_overrides[source_column]

            mapping["target_variable"] = override.get(
                "target_variable",
                mapping.get("target_variable"),
            )
            mapping["human_confirmed"] = True
            mapping["human_decision"] = override.get(
                "human_decision",
                "manually_accepted",
            )
            mapping["review_status"] = "manually_accepted"
            mapping["needs_review"] = False
            mapping["manual_override_reason"] = override.get(
                "reason",
                "Mapping was manually confirmed by creator.",
            )

        updated_mappings.append(mapping)

    updated_config["mappings"] = updated_mappings

    return updated_config
