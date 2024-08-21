import pandas as pd
from sqlalchemy import create_engine
import time
import psycopg2

df = pd.read_csv("data/oslo_met.csv") 

conn = psycopg2.connect(
    dbname='shasenem', #skal denne være individuell?
    user='shasenem',  
    password='banan2610!',
    host='localhost',
    port='5432'
)

engine = create_engine('postgresql://shasenem:banan2610!@localhost:5432/shasenem')

df.to_sql(
    name="oslo_met_db", # table name
    con=engine,  # engine
    if_exists="append", #  If the table already exists, append
    index=False # no index
)

conn.close()

start_time = time.time()


