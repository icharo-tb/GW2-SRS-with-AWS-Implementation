from airflow import DAG
from airflow.operators.python import PythonOperator # Task decorator over PythonOperator
from airflow.decorators import task

from datetime import datetime,timedelta
import time

import logging
import logging.config

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

    logging.config.fileConfig("../config/logging.conf")

    """Python Task Decorator

    Initiate preparation task -> Check code starts

    Execute ETL process -> Runs GW2-SRS ETl processes

    End DAG -> log dag ending
    """
    
    @task(task_id='airflow_prep')
    def airflow_prep(s):
        logging.info(f'Preparing Airflow...')

        time.sleep(s)

        logging.info('Ready!')

    # T1
    airflow_prep(120)

    @task(task_id='gw2-etl')
    def exec_etl():

        boss_list = [
        'vg','gors','sab','sloth','matt','kc','xera',
        'cairn','mo','sam','dei','sh','dhuum','ca',
        'twins','q1','adina','sabir','q2'
        ]

        etl_executer(rot=boss_list)

    # T2
    exec_etl()

    @task(task_id='dag_finisher')
    def dag_end():

        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        logging.info(f'Finalization time: {current_time}')

    # T3
    dag_end()