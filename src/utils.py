import yaml
from pathlib import Path
from typing import Any, Dict, Union

def load_yaml(path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load a YAML file from the given path and return its contents as a dict.
    Raises FileNotFoundError if the file does not exist.
    """
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(f"YAML file not found: {file_path}")
    with file_path.open('r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, dict) else {}