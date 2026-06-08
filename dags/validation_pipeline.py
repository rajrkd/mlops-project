from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'mlops_team',
    'depends_on_past': False,
    'start_date': datetime(2026, 6, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'mlops_data_ingestion_check',
    default_args=default_args,
    description='Automated pipeline baseline check',
    schedule_interval=None,
    catchup=False,
) as dag:

    test_task = BashOperator(
        task_id='verify_dataset_presence',
        bash_command='ls -l /opt/airflow/dags',
    )
