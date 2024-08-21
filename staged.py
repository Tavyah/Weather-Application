import os
import pandas as pd
import psycopg2 as ps
import configparser
from sqlalchemy import create_engine


CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_OUTPUT = '/data/'
FILENAME_INPUT_OSLO = 'oslo'
FILENAME_INPUT_STOCKHOLM = 'stockholm'

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

def process_and_insert(file_path, table_name):

  weather_data = pd.read_csv(file_path, sep=",")
  weather_data.to_sql(name=table_name, con=postgres_engine, if_exists="replace", index=False)

oslo_data_path = CURR_DIR_PATH + DATA_OUTPUT + FILENAME_INPUT_OSLO + '_met.csv'
process_and_insert(oslo_data_path, "met_oslo")

stockholm_data_path = CURR_DIR_PATH + DATA_OUTPUT + FILENAME_INPUT_STOCKHOLM + '_met.csv'
process_and_insert(stockholm_data_path, "met_stockholm")

oslo_data_path = CURR_DIR_PATH + DATA_OUTPUT + FILENAME_INPUT_OSLO + '_smhi.csv'
process_and_insert(oslo_data_path, "smhi_oslo")

oslo_data_path = CURR_DIR_PATH + DATA_OUTPUT + FILENAME_INPUT_OSLO + '_smhi.csv'
process_and_insert(oslo_data_path, "smhi_stockholm")

