from pathlib import Path
from typing import Union

import pandas as pd


def load_raw_data(file_path: Union[str, Path]) -> pd.DataFrame:
    """
    Load a raw clinical-style dataset from CSV or Excel.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.suffix.lower() == ".csv":
        return pd.read_csv(file_path, dtype=str)

    if file_path.suffix.lower() in [".xlsx", ".xls"]:
        return pd.read_excel(file_path, dtype=str)

    raise ValueError(f"Unsupported file type: {file_path.suffix}")


def scan_metadata(file_path: Union[str, Path]) -> dict:
    """
    Scan a raw dataset and return column-level metadata.
    """
    file_path = Path(file_path)
    df = load_raw_data(file_path)

    metadata = {
        "file_name": file_path.name,
        "n_rows": int(len(df)),
        "n_columns": int(len(df.columns)),
        "columns": [],
    }

    for column in df.columns:
        series = df[column]

        column_profile = {
            "column_name": str(column),
            "dtype": str(series.dtype),
            "missing_count": int(series.isna().sum()),
            "missing_rate": round(float(series.isna().mean()), 4),
            "unique_count": int(series.nunique(dropna=True)),
            "sample_values": series.dropna().astype(str).head(5).tolist(),
        }

        metadata["columns"].append(column_profile)

    return metadata
