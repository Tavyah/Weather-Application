import requests, os, configparser
import pandas as pd
import json

CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_OUTPUT = CURR_DIR_PATH + '/data/'
FILENAME_OUTPUT_MET = 'weather_output_met.json'

geo_locations = {
    "Oslo": (59.9, 10.8),
    "Stockholm": (59.3, 18.1)
}

def _get_weather_data(lat, lon):
    headers = {
        'User-Agent': 'MyWeatherApp/1.0 (paal.runde@gmail.com)' 
    }
    r = requests.get(f'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat}&lon={lon}', headers=headers)
    
    if r.status_code == 200:
        return r.json()
    else:
        print(f"Error: Received status code {r.status_code}")

def _write_weather_log():
    all_weather_data = []

    for city, (lat, lon) in geo_locations.items():
        weather_data = _get_weather_data(lat, lon)

        all_weather_data.append({"city": city, "weather_data": weather_data})

        with open(DATA_OUTPUT + FILENAME_OUTPUT_MET, 'w') as json_file:
            json.dump(all_weather_data, json_file)

_write_weather_log()