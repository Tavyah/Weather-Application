from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from datetime import datetime
from random import randint
from airflow.operators.bash import BashOperator

#Våre egne imports 
import extract_data as get_from_api


#Her kommer funksjonen for API get request som henter og lagrer data i rå format: 
#Den kan enten importeres eller skrives direkte inn i dokumentet
def _extract_data():
    get_from_api._get_weather_data()
    get_from_api._get_weather_data()
    get_from_api._write_weather_log()
    get_from_api._write_weather_log()
	#### Koden fra Python filene


#Her kommer funksjonen for Harmonazing and Cleansing av rå data. For enkelthetens skyld som 1 steg
def _transform_data():
   pass
    #### Hvordan kan vi slå sammen hele prosessen i en funksjon?


#Her kommer funksjonen for Staging med Postgres SQL: 
def _load_data():
    pass
	####Ny kode laget med Postgres 


with DAG("weatherAPI_dag", start_date=datetime(2021, 1, 1),
         schedule_interval="@hourly", catchup=False) as dag:

 extract_data = PythonOperator(
        task_id="extract_data",
        python_callable=_extract_data 	#referer til funksjonen ovenfor
    )

transform_data = PythonOperator(
        task_id="transform_data",
        python_callable= _transform_data 	#referer til funksjonen ovenfor 
    )

load_data= PythonOperator(
        task_id="load_data",
        python_callable= _load_data 		#referer til funksjonen ovenfor
    )

[extract_data >> transform_data >> load_data]

