import os
import pandas as pd
import psycopg2 as ps
import configparser
from sqlalchemy import create_engine


CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_OUTPUT = '/data/'

config = configparser.ConfigParser()

config.read(CURR_DIR_PATH + "/config.ini")
db_pw = config.get("DEV", "weather_data_db_pw")
db_user = config.get('DEV', 'weather_data_db_user')

def postgres_creator() -> ps:

  return ps.connect(
        dbname="weather_db",  
        user=db_user,
        password=db_pw,
        port=5433,
        host="localhost"
  )

postgres_engine = create_engine(
    url="postgresql+psycopg2://localhost",
    creator=postgres_creator
)

def process_and_insert(city_weather_service, table_name):
  data_path = CURR_DIR_PATH + DATA_OUTPUT + city_weather_service
  weather_data = pd.read_csv(data_path, sep=",")
  weather_data.to_sql(name=table_name, con=postgres_engine, if_exists="replace", index=False)





