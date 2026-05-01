# Medical Data Agent

A local-first medical data analysis agent prototype for automated data mapping  
ADSL-like dataset generation  
TLF production  
CSR-style report writing  
and audit-ready traceability

## Project Status

This project is currently an early-stage prototype

The current version supports an end-to-end demo pipeline from a raw clinical-style CSV file to a standardized analysis-ready dataset and a mini CSR-style report

## Current Pipeline

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

## Core Features Implemented

### 1. Metadata Scanner

Scans raw client-style datasets and profiles each column

Current outputs include

- column name
- data type
- missing count
- missing rate
- unique count
- sample values

### 2. Semantic Mapping Engine

Generates a draft mapping from raw source columns to ADaM-like target variables

Example mappings

| Raw Column | Target Variable |
|---|---|
| Subject_No | SUBJID |
| PT_GENDER | SEX |
| Age | AGE |
| Treatment_Group | TRT01P |
| Baseline_SBP | BASELINE |
| Followup_SBP | AVAL |

### 3. Human-in-the-loop Mapping Review

High-confidence mappings are auto-accepted  
Lower-confidence mappings require manual confirmation before entering the analysis-ready dataset

Current review logic

| Decision Type | Meaning |
|---|---|
| auto_accepted | High-confidence mapping accepted automatically |
| manually_accepted | Mapping confirmed by user review |
| pending_review | Mapping requires human review |
| unmapped | No valid target variable identified |

### 4. Mapping QC Report

Generates a mapping QC report with

- source column
- target variable
- confidence score
- human decision
- review status
- risk level
- QC message

### 5. Data Quality Report

Generates a basic data quality report with

- raw dataset row count
- raw dataset column count
- ADSL-like dataset row count
- ADSL-like dataset column count
- duplicate subject ID check
- missing rate by confirmed analysis variable

### 6. ADSL-like Dataset Builder

Uses confirmed mappings only to generate an analysis-ready dataset

Current ADSL-like variables

| Variable | Meaning |
|---|---|
| SUBJID | Subject identifier |
| SEX | Standardized sex variable |
| AGE | Subject age |
| TRT01P | Planned treatment group |
| BASELINE | Baseline measurement |
| AVAL | Analysis value |

### 7. Value Mapping

Standardizes raw coded values into analysis-ready values

Example

| Raw Value | Standard Value |
|---|---|
| 1 | M |
| 2 | F |

### 8. Table 1 Generator

Generates a demographics and baseline characteristics table

Current outputs include

- N
- age mean and SD
- age median minimum and maximum
- sex n and percentage
- baseline SBP mean and SD

### 9. Mini CSR-style Report Writer

Generates a structured mini report with

- data standardization summary
- analysis population
- demographics and baseline characteristics
- interpretation
- traceability notes

## Repository Structure

```text
medical-data-agent/
│
├── main.py
├── app.py
├── config.yaml
├── requirements.txt
├── README.md
│
├── data/
│   ├── demo/
│   └── adam_like/
│
├── outputs/
│   ├── audit_logs/
│   ├── tables/
│   └── reports/
│
└── src/
    ├── mapping/
    │   ├── metadata_scanner.py
    │   ├── semantic_matcher.py
    │   ├── mapping_config_manager.py
    │   ├── mapping_reviewer.py
    │   ├── mapping_qc.py
    │   └── value_mapper.py
    │
    ├── standards/
    │   └── adsl_builder.py
    │
    ├── tlfs/
    │   └── table_one.py
    │
    ├── audit/
    │   └── data_quality_report.py
    │
    └── report/
        └── mini_csr_writer.py
```

## How to Run

Create and activate a Python virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the demo pipeline

```bash
python main.py
```

## Demo Input

The demo raw dataset is located at

```text
data/demo/demo_raw.csv
```

## Demo Outputs

The current pipeline generates the following outputs

| Output | Path |
|---|---|
| Mapping config | outputs/audit_logs/mapping_config_demo.json |
| Mapping QC report | outputs/audit_logs/mapping_qc_report_demo.csv |
| Data quality report | outputs/audit_logs/data_quality_report_demo.csv |
| ADSL-like dataset | data/adam_like/adsl_demo.csv |
| Table 1 | outputs/tables/table_one_demo.csv |
| Mini CSR-style report | outputs/reports/mini_csr_report_demo.md |

## Privacy and Data Handling

This project is designed as a local-first prototype

No real patient data should be committed to this repository

The current demo uses synthetic clinical-style data only

Recommended privacy rules

- do not upload real client data
- do not commit raw confidential datasets
- keep real-world datasets outside version control
- use synthetic or public datasets for demos

## Current Limitations

This is not a full CDISC-compliant implementation

Current limitations include

- no full SDTM or ADaM validation
- no true MedDRA or WHODrug coding
- no safety ADAE module yet
- no TEAE logic yet
- no efficacy statistical testing yet
- no survival analysis yet
- no Streamlit UI yet
- no local LLM integration yet
- no sentence-level report traceability yet

## Near-term Roadmap

Next planned modules

- Streamlit mapping review panel
- configurable mapping override file
- primary endpoint analysis
- safety summary table
- ADAE-like dataset builder
- data lineage report
- CSR-style report v1
- local LLM interface prototype

## Project Positioning

This project is intended to become a local regulatory-grade medical data analysis agent prototype

The long-term goal is to support

```text
Raw client data
→ automated data mapping
→ human-reviewed standardization
→ analysis-ready datasets
→ TLFs
→ CSR-style narrative generation
→ audit-ready traceability
```
