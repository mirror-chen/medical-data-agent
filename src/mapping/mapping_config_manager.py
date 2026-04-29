import json
from pathlib import Path
from typing import Any, Union


def save_mapping_config(
        mapping_draft: dict,
        output_path: Union[str, Path],
) -> None:
    """
    Save mapping draft as a JSON configuration file.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(mapping_draft, file, indent=2, ensure_ascii=False)


def load_mapping_config(config_path: Union[str, Path]) -> dict:
    """
    Load a mapping configuration JSON file.
    """
    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Mapping config not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as file:
        return json.load(file)
