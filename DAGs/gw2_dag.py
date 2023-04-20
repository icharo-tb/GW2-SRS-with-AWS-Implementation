from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime,timedelta

import os
from dotenv import load_dotenv

with DAG(
    dag_id='gw2-srs-etl'
) as dag:
    pass