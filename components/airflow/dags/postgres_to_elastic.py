import datetime as dt
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

import pandas as pd
import psycopg2 as db
from elasticsearch import Elasticsearch


DEFAULT_ARGS = {
    'owner': 'johndoe',
    'start_date': dt.datetime(2022, 4, 24),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}


def queryPostgresql():
    conn_string = "dbname='dataengineering' host='localhost' user='postgres' password='postgres'"
    conn = db.connect(conn_string)

    df = pd.read_sql("select name, city from users", conn)

    df.to_csv('postgresqldata.csv')
    print("-------Data Saved------")


def insertElasticsearch():
    es = Elasticsearch('https://elastic:espw1234@localhost:9200', 
                       ca_certs=False,
                       verify_certs=False)

    df = pd.read_csv('postgresqldata.csv')

    for i,r in df.iterrows():
        doc = r.to_json()
        res = es.index(index="frompostgresql", document=doc)
        print(res)



with DAG('MyDBdag',
         default_args=DEFAULT_ARGS,
         schedule_interval=timedelta(minutes=5),
         # '0 * * * *',
         ) as dag:
    get_data = PythonOperator(task_id='QueryPostgreSQL',
                              python_callable=queryPostgresql)

    insert_data = PythonOperator(task_id='InsertDataElasticsearch',
                                 python_callable=insertElasticsearch)

get_data >> insert_data
