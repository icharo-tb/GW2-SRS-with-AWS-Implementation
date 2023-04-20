from airflow import DAG
from airflow.operators.python import PythonOperator # task decorator over PythonOperator
from airflow.decorators import task

from datetime import datetime,timedelta
import time

import logging

from src.main import etl_executer

with DAG(
    dag_id= 'gw2-srs-etl',
    description= 'GW2-SRS ETL based on AWS S3, Docker and Airflow processes.',
    default_args={
        # email: [airflow@example]
        'depends_on_past': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=10)
    },
    start_date= datetime(2023,5,1),
    schedule_interval= '@monthly', # https://airflow.apache.org/docs/apache-airflow/1.10.1/scheduler.html
    catchup= False
) as dag:
    
    # https://airflow.apache.org/docs/apache-airflow/stable/howto/operator/python.html
    
    @task(task_id='airflow_prep')
    def airflow_prep(s):
        print(f'Preparing Airflow...')

        time.sleep(s)

        print('Ready!')

    # T1
    airflow_prep(120)

    @task(task_id='gw2-etl')
    def exec_etl():

        logging.config.fileConfig("../config/logging.conf")

        boss_list = [
        'vg','gors','sab','sloth','matt','kc','xera',
        'cairn','mo','sam','dei','sh','dhuum','ca',
        'twins','q1','adina','sabir','q2'
        ]

        etl_executer(rot=boss_list)

    # T2
    exec_etl()