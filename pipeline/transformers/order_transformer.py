import pandas as pd
import logging

logger = logging.getLogger(__name__)


def transform_orders(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Rename API fields
    df = df.rename(columns={
        "id": "order_id",
        "userId": "customer_id"
    })

    # Keep required columns
    df = df[
        ["order_id", "customer_id", "title", "body"]
    ]

    # Remove rows missing important IDs
    df = df.dropna(
        subset=["order_id", "customer_id"]
    )

    # Convert IDs to integers
    df["order_id"] = pd.to_numeric(
        df["order_id"], errors="coerce"
    )

    df["customer_id"] = pd.to_numeric(
        df["customer_id"], errors="coerce"
    )

    df = df.dropna(
        subset=["order_id", "customer_id"]
    )

    df["order_id"] = df["order_id"].astype(int)
    df["customer_id"] = df["customer_id"].astype(int)

    # Synthetic column
    df["order_status"] = "received"

    df = df.reset_index(drop=True)

    logger.info(
        f"Order transformation complete: {len(df)} rows"
    )

    return df
