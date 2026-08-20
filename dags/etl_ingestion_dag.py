from airflow.decorators import dag, task
from datetime import datetime, timedelta

from dag_utils import (
    run_customer_pipeline,
    run_product_pipeline,
    run_order_pipeline,
)

default_args = {
    "owner": "data_eng",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    dag_id="etl_ingestion_pipeline",
    default_args=default_args,
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["ingestion"],
)
def etl_ingestion_dag():

    @task
    def initialize_db():
        from pipeline.loaders.db_connection import init_db

        init_db()
        return True

    @task
    def process_customers(db_initialized):
        return run_customer_pipeline()

    @task
    def process_products(db_initialized):
        return run_product_pipeline()

    @task
    def process_orders(db_initialized):
        return run_order_pipeline()

    @task
    def summarize(customer_result, product_result, order_result):
        print("Pipeline Summary")
        print("Customers:", customer_result)
        print("Products:", product_result)
        print("Orders:", order_result)

    init_done = initialize_db()

    customer_result = process_customers(init_done)
    product_result = process_products(init_done)
    order_result = process_orders(init_done)

    summarize(
        customer_result,
        product_result,
        order_result
    )


dag = etl_ingestion_dag()
