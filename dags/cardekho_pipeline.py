"""DAG: pipeline ETL harian untuk data harga mobil bekas Cardekho."""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from scripts import pipeline

default_args = {
    "owner": "data-engineering",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
    "email_on_failure": False,
}

with DAG(
    dag_id="cardekho_pipeline",
    description="ETL harian: Cardekho CSV -> Parquet -> PostgreSQL -> analytics",
    default_args=default_args,
    start_date=datetime(2026, 11, 1),
    schedule="@daily",
    catchup=False,
    tags=["cardekho", "etl", "portfolio"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract",
        python_callable=pipeline.run_extract,
    )

    transform_task = PythonOperator(
        task_id="transform",
        python_callable=pipeline.run_transform,
    )

    load_task = PythonOperator(
        task_id="load",
        python_callable=pipeline.run_load,
    )

    analytics_task = PythonOperator(
        task_id="analytics",
        python_callable=pipeline.run_analytics,
    )

    extract_task >> transform_task >> load_task >> analytics_task
