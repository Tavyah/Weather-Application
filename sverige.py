import requests, os
from typing import Callable
import json
import pandas as pd

CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_OUTPUT = '/data/'
FILENAME_OUTPUT_SWEDEN = 'weather_output_smhi.json'

geo_locations = {
    "Oslo": (59.9, 17.6),
    "Stockholm": (43, 34.32)
}

def _fetch_weather_api_sweden(lat: float, lon: float) -> str:
    return f'https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/{lon}/lat/{lat}/data.json'
        
def _get_requests_api_weather(api_call: Callable) -> requests:
    r = requests.get(api_call)
    if r.status_code == 200:
        return r.json()
    else:
        return f'Error: Recieved status code {r.status_code}'

def write_weather_log():
    locations = []
    for city, (lat, lon) in geo_locations.items():
        weather_data = _fetch_weather_api_sweden(lat, lon)
        
        locations.append({"city": city, "weather_data": _get_requests_api_weather(weather_data)})
        
    with open(CURR_DIR_PATH + DATA_OUTPUT + FILENAME_OUTPUT_SWEDEN, 'w') as file:
        file.write(json.dumps(locations))
    file.close()

write_weather_log()
