from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def run_ingestion():
    print("Starting Football Data Ingestion...")


with DAG(
    dag_id="football_pipeline_real",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    ingestion = PythonOperator(
        task_id="ingestion",
        python_callable=run_ingestion,
    )