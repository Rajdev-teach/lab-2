import pandas as pd
import logging

logger = logging.getLogger(__name__)


def transform_products(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    allowed_categories = {
        "electronics",
        "kitchen",
        "furniture"
    }

    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Clean product names
    df["name"] = df["name"].astype("string").str.strip()

    # Normalize categories
    df["category"] = (
        df["category"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    # Remove duplicate product IDs
    df = df.drop_duplicates(subset=["product_id"], keep="first")

    # Convert numeric columns
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["stock"] = pd.to_numeric(df["stock"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

    # Missing stock becomes 0
    df["stock"] = df["stock"].fillna(0).astype(int)

    # Apply business rules
    df = df[df["price"] > 0]
    df = df[df["rating"].between(0, 5)]
    df = df[df["category"].isin(allowed_categories)]

    # Convert date
    df["created_at"] = pd.to_datetime(
        df["created_at"],
        errors="coerce"
    )

    df = df.reset_index(drop=True)

    logger.info(f"Product transformation complete: {len(df)} rows")

    return df
