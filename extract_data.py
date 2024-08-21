import requests, os
from typing import Callable
import json
import pandas as pd

CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_OUTPUT = CURR_DIR_PATH + '/data/'

if not os.path.exists(DATA_OUTPUT):
    os.makedirs(DATA_OUTPUT)

geo_locations = {
    "Oslo": (59.9, 10.8),
    "Stockholm": (59.3, 18.1)
}
    
def _get_weather_data(lat, lon, weather_service):
    
    if weather_service == 'met':
        headers = {
            'User-Agent': 'MyWeatherApp/1.0 (paal.runde@gmail.com)' 
        }
        r = requests.get(f'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat}&lon={lon}', headers=headers)
    elif weather_service == 'smhi':
        r = requests.get(f'https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/{lon}/lat/{lat}/data.json')

    if r.status_code == 200:
        return r.json()
    else:
        print(f"Error: Received status code {r.status_code}")

def _write_weather_log(weather_service):
    all_weather_data = []

    for city, (lat, lon) in geo_locations.items():
        print(f"Fetching data for {city} from {weather_service}...")
        weather_data = _get_weather_data(lat, lon, weather_service)
        all_weather_data.append({"city": city, "weather_data": weather_data})
        
    output_file = DATA_OUTPUT + f'weather_output_{weather_service}.json'
    with open(output_file, 'w') as json_file:
        json.dump(all_weather_data, json_file)
    print(f"Weather data for {weather_service} written to {output_file}")

