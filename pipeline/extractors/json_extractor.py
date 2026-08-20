import json
import pandas as pd
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def extract_json(file_path: str, record_path: Optional[str] = None) -> pd.DataFrame:
    path = Path(file_path)

    if not path.exists():
        logger.error(f"File not found: {path.absolute()}")
        raise FileNotFoundError(f"Missing file: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if record_path:
            path_list = record_path.split(".")
            df = pd.json_normalize(data, record_path=path_list)
        elif isinstance(data, (dict, list)):
            df = pd.json_normalize(data)
        else:
            raise TypeError(f"Unsupported JSON root type: {type(data).__name__}")

        logger.info(f"Extracted {df.shape[0]} rows from JSON {path}")
        return df

    except (json.JSONDecodeError, TypeError, ValueError) as e:
        logger.error(f"Failed to parse/normalize JSON {path}: {e}")
        raise
