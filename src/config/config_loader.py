from pathlib import Path
from typing import Union

import yaml


def load_config(config_path: Union[str, Path] = "config.yaml") -> dict:
    """
    Load project configuration from a YAML file.
    """
    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if config is None:
        raise ValueError(f"Config file is empty: {config_path}")

    return config


def get_path(config: dict, path_key: str) -> str:
    """
    Get a configured file path from the paths section.
    """
    paths = config.get("paths", {})

    if path_key not in paths:
        raise KeyError(f"Path key not found in config: {path_key}")

    return paths[path_key]


def get_auto_accept_threshold(config: dict) -> float:
    """
    Get mapping auto-accept threshold from config.
    """
    return float(
        config.get("mapping_review", {}).get("auto_accept_threshold", 0.90)
    )


def get_manual_overrides(config: dict) -> dict:
    """
    Get manual mapping override decisions from config.
    """
    return config.get("manual_overrides", {})


def get_endpoint_config(config: dict) -> dict:
    """
    Get endpoint configuration.
    """
    endpoint_config = config.get("endpoint", {})

    required_keys = [
        "primary_endpoint_name",
        "baseline_variable",
        "analysis_variable",
        "treatment_variable",
    ]

    missing_keys = [
        key for key in required_keys
        if key not in endpoint_config
    ]

    if missing_keys:
        raise KeyError(f"Missing endpoint config keys: {missing_keys}")

    return endpoint_config


def get_safety_config(config: dict) -> dict:
    """
    Get safety configuration.
    """
    return config.get("safety", {})
