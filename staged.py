import os
import pandas as pd
import psycopg2 as ps
import configparser
from sqlalchemy import create_engine


CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

config = configparser.ConfigParser()

config.read(CURR_DIR_PATH + "/config.ini")
db_pw = config.get("DEV", "weather_data_db_pw")
db_user = config.get('DEV', 'weather_data_db_user')

def postgres_creator():
  return ps.connect(
        dbname="weather_app_db",  
        user=db_user,
        password=db_pw,
        host="localhost"
  )

postgres_engine = create_engine(
    url="postgresql+psycopg2://localhost",
    creator=postgres_creator
)

# Data processing
#TODO READ FROM DF
weather_data = pd.DataFrame()

weather_data.to_sql(name="weather_data", con=postgres_engine, if_exists="replace", index=False)