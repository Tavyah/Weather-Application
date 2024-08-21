from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from datetime import datetime
from airflow.operators.bash import BashOperator
import os

from weather_app import extract_data as get_from_api
from weather_app import harmonization as harmonization
from weather_app import staged as staged


#Her kommer funksjonen for API get request som henter og lagrer data i rå format: 
#Den kan enten importeres eller skrives direkte inn i dokumentet
def _extract_data():
    print("Starting data extraction...")
    get_from_api._write_weather_log('smhi')
    get_from_api._write_weather_log('met')
    print("Data extraction completed.")

#Her kommer funksjonen for Harmonazing and Cleansing av rå data. For enkelthetens skyld som 1 steg
def _transform_data():
    print("Current working directory:", os.getcwd())
    harmonization.process_met_weather_data('Oslo')
    harmonization.process_met_weather_data('Stockholm')
    harmonization.process_smhi_weather_data('Oslo')
    harmonization.process_smhi_weather_data('Stockholm')


#Her kommer funksjonen for Staging med Postgres SQL: 
def _load_data():
    staged.process_and_insert('oslo_met.csv', 'oslo_met')
    staged.process_and_insert('oslo_smhi.csv', 'oslo_smhi')
    staged.process_and_insert('stockholm_met.csv', 'stockholm_met')
    staged.process_and_insert('stockholm_smhi.csv', 'stockholm_smhi')


with DAG("weatherAPI_dag", start_date=datetime(2021, 1, 1),
         schedule_interval="@hourly", catchup=False) as dag:

    extract_data = PythonOperator(
        task_id="extract_data",
        python_callable=_extract_data
    )

    transform_data = PythonOperator(
        task_id="transform_data",
        python_callable= _transform_data
    )

    load_data= PythonOperator(
        task_id="load_data",
        python_callable= _load_data 
    )

extract_data >> transform_data >> load_data