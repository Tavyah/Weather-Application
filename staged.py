import os
import pandas as pd
import psycopg2 as ps
import configparser
from sqlalchemy import create_engine


CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_OUTPUT = '/data/'
FILENAME_INPUT_MET = 'oslo_met.csv'

config = configparser.ConfigParser()

config.read(CURR_DIR_PATH + "/config.ini")
db_pw = config.get("DEV", "weather_data_db_pw")
db_user = config.get('DEV', 'weather_data_db_user')

def postgres_creator() -> ps:
  return ps.connect(
        dbname="weather_db",  
        user=db_user,
        password=db_pw,
        host="localhost"
  )

postgres_engine = create_engine(
    url="postgresql+psycopg2://localhost",
    creator=postgres_creator
)

# Data processing
#TODO READ FROM DF OR CSV?
weather_data_path = CURR_DIR_PATH + DATA_OUTPUT + FILENAME_INPUT_MET

weather_data = pd.read_csv(
    weather_data_path,
    sep=","
)

data = weather_data.to_sql(name="weather_db", con=postgres_engine, if_exists="replace", index=False)

print(weather_data)
# Change dbname to be the name of your schema and user to be the owner of said database schema
conn = ps.connect(dbname="weather_db", user=db_user)
 
cur = conn.cursor()
 
cur.execute("CREATE TABLE IF NOT EXISTS weather_data (id SERIAL PRIMARY KEY, time VARCHAR(30),air_pressure_at_sea_level DECIMAL,air_temperature DECIMAL,cloud_area_fraction DECIMAL,relative_humidity DECIMAL,wind_from_direction DECIMAL,wind_speed DECIMAL,next_1_hours_precipitation_amount DECIMAL);")
 
cur.execute("INSERT INTO weather_data (time, air_pressure_at_sea_level, air_temperature,cloud_area_fraction,relative_humidity,wind_from_direction,wind_speed,next_1_hours_precipitation_amount) VALUES ('%s, %s, %s, %s, %s, %s, %s, %s');", 
            (data))
cur.execute("SELECT * FROM weather_data;")
 
cur.fetchone()
 
conn.commit()
 
cur.close()
conn.close()