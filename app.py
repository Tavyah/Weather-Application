import requests, os, configparser
import pandas as pd
import json

CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

# Initializes configuration from the config.ini file
config = configparser.ConfigParser()
config.read(CURR_DIR_PATH + "/config.ini")

geo_locations = {
    "uppsala": (59.9, 17.6),
    "östersund": (63.2, 14.6),
    "luleå": (65.6, 22.1),
    "göteborg": (57.7, 12),
    "oslo": (59.9, 10.8)
}

# Fetches the api key from your config.ini file

def _write_weather_log():

    r = requests.get('https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=59.9&lon=10.8')

    weather_df = r.json()
    weather_df = pd.DataFrame(weather_df)
    weather_df.to_json(CURR_DIR_PATH + '/weather-output.json', index=False)

_write_weather_log()

def _write_weather_log2():

    r = requests.get('https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/10.8/lat/59.9/data.json')

    weather_df = pd.DataFrame(r)
    weather_df.to_json(CURR_DIR_PATH + '/weather-output.json', index=False)

_write_weather_log2()



        

    


