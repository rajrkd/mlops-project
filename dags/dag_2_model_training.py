from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    'mlops_02_model_training',
    start_date=datetime(2026, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    # Triggers your working python script inside the container via bash
    #task_train = BashOperator(
    #    task_id='execute_pyspark_training',
    #    bash_command='docker exec mlops_pyspark_workspace python /home/jovyan/work/train.py'
    #)

    task_dvc_pull = BashOperator(
         task_id='dvc_pull_data',
         bash_command='docker exec mlops_pyspark_workspace dvc pull'
    )

    task_train = BashOperator(
         task_id='execute_pyspark_training',
         bash_command='docker exec mlops_pyspark_workspace python /home/jovyan/work/train.py'
    )

# Force DVC pull to execute before training starts
    task_dvc_pull >> task_train
