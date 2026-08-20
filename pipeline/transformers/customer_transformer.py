import pandas as pd
import logging

logger = logging.getLogger(__name__)


def transform_customers(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Remove exact duplicates
    df = df.drop_duplicates()

    # Normalize text
    df["first_name"] = df["first_name"].astype("string").str.strip().str.title()
    df["last_name"] = df["last_name"].astype("string").str.strip().str.title()
    df["email"] = df["email"].astype("string").str.strip().str.lower()

    # Convert dates
    df["signup_date"] = pd.to_datetime(
        df["signup_date"],
        errors="coerce",
        format="mixed"
    )

    # Convert numeric columns
    df["annual_spend"] = pd.to_numeric(
        df["annual_spend"],
        errors="coerce"
    )

    # Remove rows missing important fields
    df = df.dropna(subset=["first_name", "email"])

    df = df.reset_index(drop=True)

    logger.info(f"Customer transformation complete: {len(df)} rows")

    return df
