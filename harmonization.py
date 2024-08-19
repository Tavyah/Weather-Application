import json
from sverige import write_weather_log
import requests, os
from typing import Callable
import json
import pandas as pd

CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_OUTPUT = '/data/'
FILENAME_OUTPUT_SMHI = 'weather_output_smhi.json'
FILENAME_OUTPUT_MET = 'weather_output_met.json'

write_weather_log()
FILE1 = CURR_DIR_PATH + DATA_OUTPUT + FILENAME_OUTPUT_SMHI
FILE2 = CURR_DIR_PATH + DATA_OUTPUT + FILENAME_OUTPUT_MET

files = [FILE1, FILE2]

def _read_api_file(filename: str):
    f = open(filename, 'r')
    return json.load(f)

def _separate_list_elements(filename: str) -> list:
    read_file = _read_api_file(filename)
    city_list = [pd.json_normalize(city) for city in read_file]
    return city_list

def _combine_to_dataframe(city_list: list) -> pd.DataFrame:
    combined_df = pd.concat(city_list, ignore_index=False)
    return combined_df

def write_df_to_csv():
    df = _combine_to_dataframe(_separate_list_elements(FILE1))
    df.to_csv(CURR_DIR_PATH + DATA_OUTPUT + 'weather_data.csv', index=False)

write_df_to_csv()