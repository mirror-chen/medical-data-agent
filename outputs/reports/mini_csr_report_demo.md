# Mini CSR-style Report Demo

## 1. Data Standardization Summary

The source dataset was processed through an automated data mapping workflow. Raw source columns were scanned using a metadata profiling step and mapped to an ADSL-like analysis dataset structure. The resulting analysis-ready dataset included the following confirmed variables: SUBJID, SEX, AGE, TRT01P, BASELINE, AVAL.
All generated mappings were stored in a JSON mapping configuration file to support traceability between the raw source data and the derived analysis dataset.

## 2. Analysis Population

The demo ADSL-like dataset included 5 subjects overall. The Drug A group included 3 subjects and the placebo group included 2 subjects.

## 3. Demographic and Baseline Characteristics

The mean age was 68.67 (3.51) in the Drug A group and 59.5 (2.12) in the placebo group. Overall the mean age was 65.0 (5.7).

Baseline systolic blood pressure was 154.0 (5.29) in the Drug A group and 151.5 (4.95) in the placebo group. Overall baseline systolic blood pressure was 153.0 (4.69).

## 4. Interpretation

This mini report demonstrates the first end-to-end workflow from raw client-style data to a standardized analysis-ready dataset and a structured CSR-style narrative. The current output is descriptive only and should not be interpreted as evidence of treatment effectiveness or safety.

## 5. Traceability

The following outputs were generated during this workflow:

- Mapping configuration: `outputs/audit_logs/mapping_config_demo.json`
- ADSL-like dataset: `data/adam_like/adsl_demo.csv`
- Table 1: `outputs/tables/table_one_demo.csv`

