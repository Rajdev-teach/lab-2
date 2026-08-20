import pandas as pd
from sqlalchemy.dialects.postgresql import insert

from pipeline.loaders.db_connection import Customer, Product, Order


def _upsert_dataframe(session, model, df: pd.DataFrame, conflict_column: str) -> int:
    if df.empty:
        return 0

    safe = df.astype(object).where(pd.notnull(df), None)
    records = safe.to_dict(orient="records")

    table = model.__table__
    stmt = insert(table).values(records)

    pk_cols = {col.name for col in table.primary_key.columns}

    update_dict = {
        col.name: getattr(stmt.excluded, col.name)
        for col in table.columns
        if col.name not in pk_cols
    }

    upsert_stmt = stmt.on_conflict_do_update(
        index_elements=[conflict_column],
        set_=update_dict
    )

    try:
        session.execute(upsert_stmt)
        session.commit()
        return len(records)

    except Exception:
        session.rollback()
        raise


def load_customers(session, df: pd.DataFrame) -> int:
    return _upsert_dataframe(
        session,
        Customer,
        df,
        "customer_id"
    )


def load_products(session, df: pd.DataFrame) -> int:
    return _upsert_dataframe(
        session,
        Product,
        df,
        "product_id"
    )


def load_orders(session, df: pd.DataFrame) -> int:
    return _upsert_dataframe(
        session,
        Order,
        df,
        "order_id"
    )
