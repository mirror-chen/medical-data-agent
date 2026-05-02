from pprint import pprint

from src.config.config_loader import load_config
from src.config.config_loader import get_path
from src.config.config_loader import get_auto_accept_threshold
from src.config.config_loader import get_manual_overrides

from src.mapping.metadata_scanner import load_raw_data
from src.mapping.metadata_scanner import scan_metadata
from src.mapping.semantic_matcher import generate_mapping_draft
from src.mapping.mapping_reviewer import auto_confirm_high_confidence_mappings
from src.mapping.mapping_reviewer import summarize_review_status
from src.mapping.mapping_reviewer import apply_manual_overrides
from src.mapping.mapping_config_manager import save_mapping_config
from src.mapping.mapping_qc import generate_mapping_qc_report
from src.mapping.mapping_qc import save_mapping_qc_report

from src.standards.adsl_builder import build_adsl_like_dataset
from src.standards.adsl_builder import save_adsl_like_dataset

from src.audit.data_quality_report import generate_data_quality_report
from src.audit.data_quality_report import save_data_quality_report

from src.tlfs.table_one import create_demographics_baseline_table
from src.tlfs.table_one import save_table

from src.report.mini_csr_writer import generate_mini_csr_report

from src.config.config_loader import get_endpoint_config

from src.efficacy.adeff_builder import build_adeff_like_dataset
from src.efficacy.adeff_builder import save_adeff_like_dataset

from src.tlfs.primary_endpoint_table import summarize_endpoint_by_group
from src.tlfs.primary_endpoint_table import save_primary_endpoint_table

from src.efficacy.treatment_difference import calculate_treatment_difference
from src.efficacy.treatment_difference import save_treatment_difference_table

from src.efficacy.statistical_tests import welch_ttest_chg
from src.efficacy.statistical_tests import save_exploratory_ttest_table

if __name__ == "__main__":
    config = load_config("config.yaml")

    raw_data_path = get_path(config, "raw_data_path")
    mapping_config_path = get_path(config, "mapping_config_path")
    mapping_qc_output_path = get_path(config, "mapping_qc_output_path")
    data_quality_output_path = get_path(config, "data_quality_output_path")
    adsl_output_path = get_path(config, "adsl_output_path")
    adeff_output_path = get_path(config, "adeff_output_path")
    table_one_output_path = get_path(config, "table_one_output_path")
    primary_endpoint_table_output_path = get_path(
        config,
        "primary_endpoint_table_output_path",
    )

    treatment_difference_output_path = get_path(
        config,
        "treatment_difference_output_path",
    )

    exploratory_ttest_output_path = get_path(
        config,
        "exploratory_ttest_output_path",
    )

    report_output_path = get_path(config, "report_output_path")

    auto_accept_threshold = get_auto_accept_threshold(config)
    manual_overrides = get_manual_overrides(config)
    endpoint_config = get_endpoint_config(config)

    metadata = scan_metadata(raw_data_path)
    mapping_draft = generate_mapping_draft(metadata)

    reviewed_mapping_config = auto_confirm_high_confidence_mappings(
        mapping_draft,
        auto_accept_threshold=auto_accept_threshold,
    )

    reviewed_mapping_config = apply_manual_overrides(
        reviewed_mapping_config,
        manual_overrides,
    )

    review_summary = summarize_review_status(reviewed_mapping_config)

    save_mapping_config(reviewed_mapping_config, mapping_config_path)

    mapping_qc_report = generate_mapping_qc_report(reviewed_mapping_config)
    save_mapping_qc_report(mapping_qc_report, mapping_qc_output_path)

    adsl_df = build_adsl_like_dataset(
        raw_data_path=raw_data_path,
        mapping_config_path=mapping_config_path,
    )

    save_adsl_like_dataset(adsl_df, adsl_output_path)

    adeff_df = build_adeff_like_dataset(
        adsl_df=adsl_df,
        endpoint_config=endpoint_config,
    )

    save_adeff_like_dataset(
        adeff_df,
        adeff_output_path,
    )

    primary_endpoint_table = summarize_endpoint_by_group(adeff_df)

    save_primary_endpoint_table(
        primary_endpoint_table,
        primary_endpoint_table_output_path,
    )

    treatment_difference_table = calculate_treatment_difference(
        adeff_df=adeff_df,
        endpoint_config=endpoint_config,
    )

    save_treatment_difference_table(
        treatment_difference_table,
        treatment_difference_output_path,
    )

    exploratory_ttest_table = welch_ttest_chg(
        adeff_df=adeff_df,
        endpoint_config=endpoint_config,
    )

    save_exploratory_ttest_table(
        exploratory_ttest_table,
        exploratory_ttest_output_path,
    )

    raw_df = load_raw_data(raw_data_path)

    data_quality_report = generate_data_quality_report(
        raw_df=raw_df,
        adsl_df=adsl_df,
    )

    save_data_quality_report(
        data_quality_report,
        data_quality_output_path,
    )

    table_one = create_demographics_baseline_table(adsl_df)
    save_table(table_one, table_one_output_path)

    output_files = {
        "Mapping configuration": mapping_config_path,
        "Mapping QC report": mapping_qc_output_path,
        "Data quality report": data_quality_output_path,
        "ADSL-like dataset": adsl_output_path,
        "ADEFF-like dataset": adeff_output_path,
        "Table 1": table_one_output_path,
        "Primary endpoint table": primary_endpoint_table_output_path,
        "Treatment difference table": treatment_difference_output_path,
        "Exploratory t-test table": exploratory_ttest_output_path,
    }

    mini_report = generate_mini_csr_report(
        table_one=table_one,
        output_path=report_output_path,
        adsl_columns=adsl_df.columns.tolist(),
        primary_endpoint_table=primary_endpoint_table,
        treatment_difference_table=treatment_difference_table,
        output_files=output_files,
    )

    print("\nMapping review summary:")
    print(review_summary)

    print(f"\nMapping config saved to: {mapping_config_path}")
    print(f"Mapping QC report saved to: {mapping_qc_output_path}")
    print(f"Data quality report saved to: {data_quality_output_path}")
    print(f"ADSL-like dataset saved to: {adsl_output_path}")
    print(f"ADEFF-like dataset saved to: {adeff_output_path}")
    print(f"Primary endpoint table saved to: {primary_endpoint_table_output_path}")
    print(f"Treatment difference table saved to: {treatment_difference_output_path}")
    print(f"Exploratory t-test table saved to: {exploratory_ttest_output_path}")
    print(f"Table 1 saved to: {table_one_output_path}")
    print(f"Mini CSR-style report saved to: {report_output_path}")

    print("\nReviewed mapping config:")
    pprint(reviewed_mapping_config)

    print("\nMapping QC report preview:")
    print(mapping_qc_report)

    print("\nData quality report preview:")
    print(data_quality_report)

    print("\nADSL-like dataset preview:")
    print(adsl_df)

    print("\nADEFF-like dataset preview:")
    print(adeff_df)

    print("\nPrimary endpoint table preview:")
    print(primary_endpoint_table)

    print("\nTreatment difference table preview:")
    print(treatment_difference_table)

    print("\nExploratory t-test table preview:")
    print(exploratory_ttest_table)

    print("\nTable 1 preview:")
    print(table_one)

    print("\nMini report preview:")
    print(mini_report)
