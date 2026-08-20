from pipeline.extractors.csv_extractor import extract_csv
from pipeline.extractors.json_extractor import extract_json
from pipeline.extractors.api_extractor import extract_api

from pipeline.transformers.customer_transformer import transform_customers
from pipeline.transformers.product_transformer import transform_products
from pipeline.transformers.order_transformer import transform_orders

from pipeline.loaders.db_connection import SessionLocal
from pipeline.loaders.db_loader import load_customers, load_products, load_orders


def run_customer_pipeline():
    raw = extract_csv("data/raw/customers.csv")
    clean = transform_customers(raw)

    with SessionLocal() as session:
        loaded = load_customers(session, clean)

    return {
        "raw": len(raw),
        "clean": len(clean),
        "loaded": loaded
    }


def run_product_pipeline():
    raw = extract_json("data/raw/products.json")
    clean = transform_products(raw)

    with SessionLocal() as session:
        loaded = load_products(session, clean)

    return {
        "raw": len(raw),
        "clean": len(clean),
        "loaded": loaded
    }


def run_order_pipeline():
    raw = extract_api(
        "https://jsonplaceholder.typicode.com/posts"
    )
    clean = transform_orders(raw)

    with SessionLocal() as session:
        loaded = load_orders(session, clean)

    return {
        "raw": len(raw),
        "clean": len(clean),
        "loaded": loaded
    }
