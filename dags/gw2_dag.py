from airflow import DAG
from airflow.operators.python import PythonOperator # Task decorator over PythonOperator
from airflow.decorators import task

from datetime import datetime,timedelta
import time

import logging
import logging.config

import sys
import os

sys.path.append('/opt/airflow/src')
#sys.path.insert(0,os.path.abspath(os.path.dirname(__file__)))

from src import *
from url_writer import url_writer_script
from s3_load import s3_loader
from s3_read import s3_reader
from main_etl import gw2_etl

from config import *

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
        - URL writer
        - URL reader
        - ETL process

    End DAG -> log dag ending
        - log upload
    """
    
    @task(task_id='airflow_prep')
    def airflow_prep(s=120):
        logging.info(f'Preparing Airflow...')

        time.sleep(s)

        logging.info('Ready!')

    @task(task_id='gw2_url_loader')
    def url_loader():

        rot = [
        'vg','gors','sab','sloth','matt','kc','xera',
        'cairn','mo','sam','dei','sh','dhuum','ca',
        'twins','q1','adina','sabir','q2'
        ]

        cnt = 0

        while cnt <= 18:
            try:
                url = f'https://gw2wingman.nevermindcreations.de/content/raid/{rot[cnt]}?onlyCM=onlyNM'
                logging.info(url)
                url_writer_script(url)
            except Exception as e:
                logging.warning(e)
            finally:
                cnt += 1
                cnt % len(rot)

        try:
            s3_loader('../src/tmp/urls.txt','gw2-srs-bucket','us-east-1','urls.txt')
            logging.info('File loaded to S3.')
        except Exception as e:
            logging.warning(e)
    
    @task(task_id='gw2_etl_exec')
    def etl_exec():
        url_list = s3_reader('gw2-srs-bucket','urls.txt')

        cnt = 0

        for url in url_list:

            cnt += 1

            try:
                st_url = url.strip()
                rep = st_url.replace('log', 'logContent')
                logging.info(rep)
                gw2_etl(rep)
                logging.info(f'Log nº: {cnt}')
            except IndexError as e:
                logging.warning(e)
                continue

    @task(task_id='dag_finisher')
    def dag_end():

        now = datetime.now()
        logging.info(f'Finalization time: {now}')
    
    @task(task_id='log_loader')
    def log_loader():
        s3_loader('../src/log/gw2_srs.log','gw2-srs-logs','eu-west-3','gw2_srs.log')

    @task(task_id='file_cleaner')
    def file_cleaner():

        os.remove('../src/tmp/*')
        os.remove('../src/log/*')

        log_file = open('../src/log/gw2_srs.log', 'x')
        log_file.close()

    
    airflow_prep >> url_loader >> etl_exec >> [dag_end,log_loader] >> file_cleaner


    # docker exec -it <container_id> /bin/bash --> access bash
    # docker stop $(docker ps -a -q) --> stop all containers