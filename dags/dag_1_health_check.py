from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import requests

with DAG(
    'mlops_01_system_health',
    start_date=datetime(2026, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    def check_mlflow():
        res = requests.get("http://mlflow-server:5000/")
        if res.status_code == 200:
            print("MLflow Server is Up!")

    task_check = PythonOperator(
        task_id='ping_mlflow',
        python_callable=check_mlflow
    )
