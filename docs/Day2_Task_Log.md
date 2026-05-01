# Day 2 Task Log

## Date

Day 2

## Main Objective

The objective of Day 2 was to upgrade the mapping pipeline from a purely automatic mapping draft into a human-reviewed and audit-aware mapping workflow

The key principle implemented today was

```text
AI suggestion does not automatically become analysis-ready truth
```

Only confirmed mappings are allowed to enter the ADSL-like analysis dataset

---

## Pipeline Status After Day 2

```text
Raw CSV
→ Metadata Scanner
→ Semantic Matcher
→ Human-in-the-loop Mapping Review
→ Manual Override
→ Mapping QC Report
→ Data Quality Report
→ Mapping Config JSON
→ ADSL-like Dataset
→ Value Mapping
→ Table 1
→ Mini CSR-style Report
```

---

## Completed Tasks

### 1. Added Human-in-the-loop Mapping Fields

The semantic mapping output was upgraded with two new review fields

```text
human_confirmed
human_decision
```

These fields allow each source-to-target mapping to record whether it has been reviewed and how the decision was made

Example

```text
human_confirmed: True
human_decision: auto_accepted
```

or

```text
human_confirmed: True
human_decision: manually_accepted
```

---

### 2. Added Mapping Review Logic

Created

```text
src/mapping/mapping_reviewer.py
```

This module handles mapping review decisions

Implemented functions

```text
auto_confirm_high_confidence_mappings
summarize_review_status
apply_manual_overrides
```

The current auto-accept threshold is

```text
0.90
```

Mappings with confidence greater than or equal to 0.90 are auto-accepted

Mappings below the threshold require human review unless manually overridden

---

### 3. Added Manual Override Logic

The mapping

```text
Followup_SBP → AVAL
```

had confidence

```text
0.85
```

Because it was below the auto-accept threshold it was initially marked for review

It was then manually confirmed by the creator as the post-baseline analysis value for the demo endpoint

Final decision

```text
human_confirmed: True
human_decision: manually_accepted
review_status: manually_accepted
```

This demonstrates the first working version of the human-in-the-loop workflow

---

### 4. Updated ADSL-like Dataset Builder

Updated

```text
src/standards/adsl_builder.py
```

The ADSL-like builder now only uses confirmed mappings

Current rule

```text
Only mappings with human_confirmed = True can enter the analysis-ready dataset
```

This prevents unreviewed AI-suggested mappings from being used in downstream analysis

---

### 5. Added Mapping QC Report

Created

```text
src/mapping/mapping_qc.py
```

This module generates a mapping quality control report

Output file

```text
outputs/audit_logs/mapping_qc_report_demo.csv
```

The report includes

```text
source_column
target_variable
confidence
human_confirmed
human_decision
review_status
risk_level
qc_message
```

Current QC result

| Source Column | Target Variable | Decision | Risk Level |
|---|---|---|---|
| Subject_No | SUBJID | auto_accepted | Low |
| PT_GENDER | SEX | auto_accepted | Low |
| Age | AGE | auto_accepted | Low |
| Treatment_Group | TRT01P | auto_accepted | Low |
| Baseline_SBP | BASELINE | auto_accepted | Low |
| Followup_SBP | AVAL | manually_accepted | Medium |

---

### 6. Added Data Quality Report

Created

```text
src/audit/data_quality_report.py
```

This module generates a basic data quality report for the raw dataset and the ADSL-like dataset

Output file

```text
outputs/audit_logs/data_quality_report_demo.csv
```

The report checks

```text
raw row count
raw column count
ADSL-like row count
ADSL-like column count
duplicate subject ID
missing rate by confirmed analysis variable
```

Current result

| Check | Result |
|---|---|
| raw row count | 5 |
| raw column count | 6 |
| ADSL-like row count | 5 |
| ADSL-like column count | 6 |
| duplicate subject ID | pass |
| missing rate | 0 for all confirmed variables |

---

### 7. Updated Mini CSR-style Report Logic

Updated

```text
src/report/mini_csr_writer.py
```

The report now dynamically reads the actual confirmed variables from the ADSL-like dataset

Current confirmed variables

```text
SUBJID
SEX
AGE
TRT01P
BASELINE
AVAL
```

This prevents the report from claiming that a variable was included when it was not actually confirmed or present in the analysis dataset

---

### 8. Updated README

Updated

```text
README.md
```

The README now documents

```text
project purpose
current pipeline
implemented modules
repository structure
how to run
demo input
demo outputs
privacy rules
current limitations
near-term roadmap
```

This improves the GitHub presentation quality of the project

---

## Output Files Generated

| Output | Path |
|---|---|
| Mapping config | outputs/audit_logs/mapping_config_demo.json |
| Mapping QC report | outputs/audit_logs/mapping_qc_report_demo.csv |
| Data quality report | outputs/audit_logs/data_quality_report_demo.csv |
| ADSL-like dataset | data/adam_like/adsl_demo.csv |
| Table 1 | outputs/tables/table_one_demo.csv |
| Mini CSR-style report | outputs/reports/mini_csr_report_demo.md |

---

## Current Mapping Review Summary

```text
total_mappings: 6
auto_accepted: 5
manually_accepted: 1
pending_review: 0
manual_review_required: 0
unmapped: 0
```

Interpretation

```text
Five mappings were accepted automatically based on high confidence
One mapping was manually accepted after review
No mappings remain pending
No mappings are unmapped
```

---

## Key Technical Principle Implemented

Day 2 introduced the first audit-aware control layer

```text
AI recommends
Human confirms
Only confirmed mappings enter analysis
QC report records the decision
```

This is a core design principle for a medical data analysis system because automatic mapping errors can directly affect downstream statistical outputs and report conclusions

---

## Current Limitations

The current human-in-the-loop logic is still hard-coded in

```text
main.py
```

The manual override is currently defined as a Python dictionary

Example

```python
manual_overrides = {
    "Followup_SBP": {
        "target_variable": "AVAL",
        "human_decision": "manually_accepted",
        "reason": "Creator confirmed Followup_SBP as the post-baseline analysis value for the demo endpoint.",
    }
}
```

This should later be moved into

```text
config.yaml
```

or a Streamlit review interface

---

## Next Step

The recommended next step is configuration refactoring

Move hard-coded paths and parameters from

```text
main.py
```

into

```text
config.yaml
```

Items to configure next

```text
raw data path
mapping config path
mapping QC report path
data quality report path
ADSL-like output path
Table 1 output path
mini report output path
auto-accept threshold
manual override decisions
```

This will make the project more modular and closer to a real pipeline framework
