Production-Style ETL Data Ingestion Pipeline

Overview

This project implements an end-to-end ETL (Extract, Transform, Load) data ingestion pipeline using Python, Pandas, PostgreSQL, SQLAlchemy, and Apache Airflow.

The pipeline extracts data from multiple sources, cleans and transforms the data, loads the processed records into PostgreSQL, and orchestrates the complete workflow using Apache Airflow.

Data Sources

CSV: Customer data

JSON: Product data

REST API: Order data from JSONPlaceholder

Pipeline Architecture

CSV / JSON / REST API
        |
        v
      Extract
        |
        v
 Transform with Pandas
        |
        v
 Load with SQLAlchemy
        |
        v
    PostgreSQL
        |
        v
 Apache Airflow

Technologies Used

Python

Pandas

PostgreSQL

SQLAlchemy

Requests

Apache Airflow

Git

GitHub

Project Structure

lab-2/
├── dags/
│   ├── dag_utils.py
│   └── etl_ingestion_dag.py
├── data/
│   └── raw/
├── pipeline/
│   ├── extractors/
│   ├── transformers/
│   ├── loaders/
│   └── utils/
├── main.py
├── requirements.txt
├── .gitignore
└── README.md

ETL Process

1. Extract

The extraction layer collects data from:

Customer CSV file

Product JSON file

JSONPlaceholder REST API

2. Transform

Pandas is used for:

Duplicate removal

Missing-value handling

Data type conversion

Text normalization

Date conversion

Business-rule validation

Product category normalization

API field mapping

3. Load

The transformed data is loaded into three PostgreSQL tables:

customers

products

orders

PostgreSQL UPSERT logic makes repeated pipeline runs idempotent and prevents duplicate primary-key records.

Apache Airflow

The ETL pipeline is orchestrated using the Apache Airflow TaskFlow API.

DAG ID: etl_ingestion_pipeline

DAG Workflow

initialize_db
      |
      +--------------------+
      |          |         |
      v          v         v
 customers   products   orders
      |          |         |
      +----------+---------+
                 |
                 v
             summarize

The DAG includes daily scheduling and retry handling.

Pipeline Results

Dataset

Raw

Clean

Loaded

Customers

8

6

6

Products

8

6

6

Orders

100

100

100

The complete Airflow DAG test finished successfully.

Run the Standalone Pipeline

Activate the virtual environment:

source .venv/bin/activate

Run the ETL pipeline:

python main.py

Test the Airflow DAG

export PYTHONPATH=$(pwd)
export AIRFLOW_HOME=$(pwd)
export AIRFLOW__CORE__LOAD_EXAMPLES=False

airflow dags test etl_ingestion_pipeline 2026-08-20

Database Verification

Connect to PostgreSQL:

psql -h /tmp -p 5433 -d ingestion_db

Verify the loaded records:

SELECT COUNT(*) FROM customers;
SELECT COUNT(*) FROM products;
SELECT COUNT(*) FROM orders;

Expected results:

Customers: 6

Products: 6

Orders: 100

Logging

The project includes logging for extraction, transformation, loading, errors, and pipeline execution information.

Local runtime logs are excluded from Git using .gitignore.

Key Features

Multi-source data ingestion

Reusable extractors and transformers

Data cleaning with Pandas

PostgreSQL relational storage

SQLAlchemy ORM

Idempotent UPSERT loading

Logging and error handling

Apache Airflow TaskFlow orchestration

Task dependencies

Daily scheduling and retries