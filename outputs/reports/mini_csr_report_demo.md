# Mini CSR-style Report Demo

## 1. Data Standardization Summary

The source dataset was processed through an automated data mapping workflow. Raw source columns were scanned using a metadata profiling step and mapped to an ADSL-like analysis dataset structure. The resulting analysis-ready dataset included the following confirmed variables: SUBJID, SEX, AGE, TRT01P, BASELINE, AVAL.
All generated mappings were stored in a JSON mapping configuration file to support traceability between the raw source data and the derived analysis dataset.

## 2. Analysis Population

The demo ADSL-like dataset included 5 subjects overall. The Drug A group included 3 subjects and the placebo group included 2 subjects.

## 3. Demographic and Baseline Characteristics

The mean age was 68.67 (3.51) in the Drug A group and 59.5 (2.12) in the placebo group. Overall the mean age was 65.0 (5.7).

Baseline systolic blood pressure was 154.0 (5.29) in the Drug A group and 151.5 (4.95) in the placebo group. Overall baseline systolic blood pressure was 153.0 (4.69).


## 4. Primary Endpoint Descriptive Summary

The primary endpoint was defined as Change from baseline in systolic blood pressure.

In this synthetic demo dataset, the Drug A group showed a mean change from baseline of -18.33, compared with -4.0 in the placebo group. The corresponding mean percentage change from baseline was -11.89% in the Drug A group and -2.63% in the placebo group.

The descriptive mean difference in change from baseline was -14.33, and the descriptive mean difference in percentage change from baseline was -9.26 percentage points.

These results are descriptive only. No statistical inference was performed. The observed difference should not be interpreted as confirmatory evidence of treatment effectiveness because the dataset is synthetic and the sample size is very small.


## 5. Interpretation

This mini report demonstrates the first end-to-end workflow from raw client-style data to a standardized analysis-ready dataset and a structured CSR-style narrative. The current output is descriptive only and should not be interpreted as evidence of treatment effectiveness or safety.

## 6. Traceability

The following outputs were generated during this workflow:

- Mapping configuration: `outputs/audit_logs/mapping_config_demo.json`
- Mapping QC report: `outputs/audit_logs/mapping_qc_report_demo.csv`
- Data quality report: `outputs/audit_logs/data_quality_report_demo.csv`
- ADSL-like dataset: `data/adam_like/adsl_demo.csv`
- ADEFF-like dataset: `data/adam_like/adeff_demo.csv`
- Table 1: `outputs/tables/table_one_demo.csv`
- Primary endpoint table: `outputs/tables/primary_endpoint_table_demo.csv`
- Treatment difference table: `outputs/tables/treatment_difference_demo.csv`
- Exploratory t-test table: `outputs/tables/exploratory_ttest_demo.csv`

