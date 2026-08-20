import sys
import logging

from pipeline.utils.logger import setup_logging
from pipeline.extractors.csv_extractor import extract_csv
from pipeline.extractors.json_extractor import extract_json
from pipeline.extractors.api_extractor import extract_api
from pipeline.transformers.customer_transformer import transform_customers
from pipeline.transformers.product_transformer import transform_products
from pipeline.transformers.order_transformer import transform_orders
from pipeline.loaders.db_connection import SessionLocal, init_db
from pipeline.loaders.db_loader import load_customers, load_products, load_orders

logger = logging.getLogger(__name__)


def run_pipeline():
    setup_logging()
    logger.info("Starting ETL pipeline")

    init_db()

    try:
        with SessionLocal() as session:
            customers = transform_customers(
                extract_csv("data/raw/customers.csv")
            )
            customer_count = load_customers(session, customers)
            logger.info(f"Customers loaded: {customer_count}")

            products = transform_products(
                extract_json("data/raw/products.json")
            )
            product_count = load_products(session, products)
            logger.info(f"Products loaded: {product_count}")

            orders = transform_orders(
                extract_api("https://jsonplaceholder.typicode.com/posts")
            )
            order_count = load_orders(session, orders)
            logger.info(f"Orders loaded: {order_count}")

        logger.info("ETL pipeline completed successfully")
        return 0

    except Exception:
        logger.exception("ETL pipeline failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_pipeline())
