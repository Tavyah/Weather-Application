import requests, os, configparser
import pandas as pd
import json

CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
target_path = CURR_DIR_PATH + '/data/'

def _write_weather_log():
    headers = {
        'User-Agent': 'MyWeatherApp/1.0 (paal.runde@gmail.com)' 
    }

    r = requests.get('https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=59.9&lon=10.8', headers=headers)

    if r.status_code == 200:
        weather_df = r.json()
        weather_df = pd.DataFrame(weather_df)
        weather_df.to_json(CURR_DIR_PATH + '/data/weather-output-met.json', index=False)
    else:
        print(f"Error: Received status code {r.status_code}")

_write_weather_log()