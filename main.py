from pprint import pprint

from src.mapping.metadata_scanner import scan_metadata
from src.mapping.semantic_matcher import generate_mapping_draft
from src.mapping.mapping_reviewer import auto_confirm_high_confidence_mappings
from src.mapping.mapping_reviewer import summarize_review_status
from src.mapping.mapping_config_manager import save_mapping_config
from src.standards.adsl_builder import build_adsl_like_dataset
from src.standards.adsl_builder import save_adsl_like_dataset
from src.tlfs.table_one import create_demographics_baseline_table
from src.tlfs.table_one import save_table
from src.report.mini_csr_writer import generate_mini_csr_report
from src.mapping.mapping_reviewer import apply_manual_overrides


if __name__ == "__main__":
    raw_data_path = "data/demo/demo_raw.csv"
    mapping_config_path = "outputs/audit_logs/mapping_config_demo.json"
    adsl_output_path = "data/adam_like/adsl_demo.csv"
    table_one_output_path = "outputs/tables/table_one_demo.csv"
    report_output_path = "outputs/reports/mini_csr_report_demo.md"

    metadata = scan_metadata(raw_data_path)
    mapping_draft = generate_mapping_draft(metadata)

    reviewed_mapping_config = auto_confirm_high_confidence_mappings(
        mapping_draft,
        auto_accept_threshold=0.90,
    )

    manual_overrides = {
        "Followup_SBP": {
            "target_variable": "AVAL",
            "human_decision": "manually_accepted",
            "reason": "Creator confirmed Followup_SBP as the post-baseline analysis value for the demo endpoint.",
        }
    }

    reviewed_mapping_config = apply_manual_overrides(
        reviewed_mapping_config,
        manual_overrides,
    )

    review_summary = summarize_review_status(reviewed_mapping_config)

    save_mapping_config(reviewed_mapping_config, mapping_config_path)

    adsl_df = build_adsl_like_dataset(
        raw_data_path=raw_data_path,
        mapping_config_path=mapping_config_path,
    )

    save_adsl_like_dataset(adsl_df, adsl_output_path)

    table_one = create_demographics_baseline_table(adsl_df)
    save_table(table_one, table_one_output_path)

    mini_report = generate_mini_csr_report(
        table_one=table_one,
        output_path=report_output_path,
        adsl_columns=adsl_df.columns.tolist(),
    )

    print("\nMapping review summary:")
    print(review_summary)

    print(f"\nMapping config saved to: {mapping_config_path}")
    print(f"ADSL-like dataset saved to: {adsl_output_path}")
    print(f"Table 1 saved to: {table_one_output_path}")
    print(f"Mini CSR-style report saved to: {report_output_path}")

    print("\nReviewed mapping config:")
    pprint(reviewed_mapping_config)

    print("\nADSL-like dataset preview:")
    print(adsl_df)

    print("\nTable 1 preview:")
    print(table_one)

    print("\nMini report preview:")
    print(mini_report)
