import datetime as dt
from datetime import timedelta
import json
import urllib

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
ISSUES_FILENAME = ROOT_DIRECTORY + '/output/issues.json'
TRANSFORMED_FILENAME = ROOT_DIRECTORY + '/output/transformed.json'


def downloadIssues():
    try:
        param = {'place_url': 'bernalillo-county', 'per_page': '100'}
        url = 'https://seeclickfix.com/api/v2/issues?' + urllib.parse.urlencode(param)
        rawreply = urllib.request.urlopen(url).read()
        reply = json.loads(rawreply)
        with open(ISSUES_FILENAME, 'w') as outfile:
            json.dump(reply, outfile)
    except:
        raise 'Issue Downloading From SeeClickFix Failed'


def convertDataForElasticsearch():
    f = open(ISSUES_FILENAME)
    json_data = json.load(f)
    df = pd.DataFrame(json_data['issues'])
    df['coords'] = df['lat'].astype(str) + ',' + df['lng'].astype(str)
    df['opendate'] = df['created_at'].str.split('T').str[0]
    df.to_json(TRANSFORMED_FILENAME)


def saveIssuesToElasticsearch():
    pass


with DAG('311DataPipeline',
         default_args=default_args,
         schedule_interval=timedelta(minutes=5),
         # '0 * * * *',
         ) as dag:
    getIssues = PythonOperator(task_id='retrieve', python_callable=downloadIssues)
    transformIssues = PythonOperator(task_id='transform', python_callable=convertDataForElasticsearch)
    saveIssues = PythonOperator(task_id='save', python_callable=saveIssuesToElasticsearch)


getIssues >> transformIssues >> saveIssues