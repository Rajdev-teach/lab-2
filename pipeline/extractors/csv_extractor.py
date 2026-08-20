import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def extract_csv(file_path: str, **kwargs) -> pd.DataFrame:
    path = Path(file_path)

    if not path.exists():
        logger.error(f"File not found: {path.absolute()}")
        raise FileNotFoundError(f"Missing file: {path}")

    try:
        encoding = kwargs.pop("encoding", "utf-8")

        df = pd.read_csv(path, encoding=encoding, **kwargs)

        logger.info(f"Extracted {df.shape[0]} rows from CSV {path}")
        return df

    except Exception as e:
        logger.error(f"Failed to parse CSV {path}: {e}")
        raise
