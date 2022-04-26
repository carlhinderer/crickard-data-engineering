import datetime as dt
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

import pandas as pd


default_args = {
    'owner': 'johndoe',
    'start_date': dt.datetime(2022, 4, 25),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

ROOT_DIRECTORY = '/home/carl/Code/Python/crickard-data-engineering'
ORIGINAL_FILENAME = ROOT_DIRECTORY + '/shared_data/csv/scooter.csv'
CLEAN_FILENAME = ROOT_DIRECTORY + '/output/cleanscooter.csv'
MAY_JUNE_FILENAME = ROOT_DIRECTORY + '/output/may23-june3.csv'

BASH_COMMAND = 'cp %s /home/carl/Desktop' % MAY_JUNE_FILENAME


def cleanScooter():
    df = pd.read_csv(ORIGINAL_FILENAME)
    df.drop(columns=['region_id'], inplace=True)
    df.columns = [x.lower() for x in df.columns]
    df['started_at'] = pd.to_datetime(df['started_at'], format='%m/%d/%Y %H:%M')
    df.to_csv(CLEAN_FILENAME)


def filterData():
    df = pd.read_csv(CLEAN_FILENAME)
    fromd = '2019-05-23'
    tod = '2019-06-03'
    tofrom = df[(df['started_at'] > fromd) & (df['started_at'] < tod)]
    tofrom.to_csv(MAY_JUNE_FILENAME)


with DAG('CleanData',
         default_args=default_args,
         schedule_interval=timedelta(minutes=5),
         # '0 * * * *',
         ) as dag:
    cleanData = PythonOperator(task_id='clean', python_callable=cleanScooter)
    selectData = PythonOperator(task_id='filter', python_callable=filterData)
    copyFile = BashOperator(task_id='copy', bash_command=BASH_COMMAND)


cleanData >> selectData >> copyFile