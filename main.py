from pprint import pprint

from src.mapping.metadata_scanner import scan_metadata
from src.mapping.semantic_matcher import generate_mapping_draft
from src.mapping.mapping_config_manager import save_mapping_config


if __name__ == "__main__":
    file_path = "data/demo/demo_raw.csv"
    output_path = "outputs/audit_logs/mapping_config_demo.json"

    metadata = scan_metadata(file_path)
    mapping_draft = generate_mapping_draft(metadata)

    save_mapping_config(mapping_draft, output_path)

    pprint(mapping_draft)
    print(f"\nMapping config saved to: {output_path}")
