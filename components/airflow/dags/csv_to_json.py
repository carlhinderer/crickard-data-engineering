import datetime as dt
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

import pandas as pd


ROOT_DIRECTORY = '/home/carl/Code/Python/crickard-data-engineering'
CSV_FILENAME = ROOT_DIRECTORY + '/shared_data/csv/data.csv'
JSON_FILENAME = ROOT_DIRECTORY + '/output/fromAirflow.json'


def csv_to_json():
    df = pd.read_csv(CSV_FILENAME)
    for i, r in df.iterrows():
        print(r['name'])
    df.to_json(JSON_FILENAME, orient='records')


DEFAULT_ARGS = {
    'owner': 'johndoe',
    'start_date': dt.datetime(2020, 3, 18),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5)
}

BASH_COMMAND_TEXT = 'echo "I am reading the CSV now....."'


# Create tasks
with DAG('MyCsvDag',
         default_args=DEFAULT_ARGS,
         schedule_interval=timedelta(minutes=5), 
         # '0 * * * *',
) as dag:
    print_starting_task = BashOperator(task_id='starting', bash_command=BASH_COMMAND_TEXT)
    csv_to_json_task = PythonOperator(task_id='convert_to_json', python_callable=csv_to_json)


# Define relationships between tasks
print_starting_task >> csv_to_json_task