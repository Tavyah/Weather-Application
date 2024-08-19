import requests, os, configparser
import pandas as pd
from typing import Callable

CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_OUTPUT = '/data/'
FILENAME_OUTPUT_SMHI = 'weather_output_smhi.json'
FILENAME_OUTPUT_MET = 'weather_output_met.json'

geo_locations = {
    "Oslo": (59.9, 10.8),
    "Stockholm": (43, 34.32)
}

def _fetch_weather_api_smhi(lat: float, lon: float) -> str:
    return f'https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/{lon}/lat/{lat}/data.json'
        
def _get_requests_api_weather(api_call: Callable) -> requests:
    r = requests.get(api_call)
    if r.status_code == 200:
        return r
    else:
        return f'Error: Recieved status code {r.status_code}'

def write_weather_log_smhi():
    locations = []
    for city in geo_locations:
        (lat, lon) = geo_locations[city]
        locations.append(_get_requests_api_weather(_fetch_weather_api_smhi(lat, lon)))

    weather_df = pd.DataFrame(locations)
    weather_df.to_json(CURR_DIR_PATH + DATA_OUTPUT + FILENAME_OUTPUT_SMHI, index=False)

write_weather_log_smhi()

def _write_weather_log_met():
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

_write_weather_log_met()