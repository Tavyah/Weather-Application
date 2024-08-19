import requests, os, configparser
import pandas as pd
from typing import Callable

CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_OUTPUT = '/data/'
FILENAME_OUTPUT_SWEDEN = 'weather-output_sweden.json'

geo_locations = {
    "Oslo": (59.9, 17.6),
    "Stockholm": (43, 34.32)
}

def _fetch_weather_api_sweden(lat: float, lon: float) -> str:
    return f'https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/{lon}/lat/{lat}/data.json'
        
def _get_requests_api_weather(api_call: Callable) -> requests:
    return requests.get(api_call)

def write_weather_log():
    locations = []
    for city in geo_locations:
        (lat, lon) = geo_locations[city]
        locations.append(_get_requests_api_weather(_fetch_weather_api_sweden(lat, lon)))

    weather_df = pd.DataFrame(locations)
    weather_df.to_json(CURR_DIR_PATH + DATA_OUTPUT + FILENAME_OUTPUT_SWEDEN, index=False)

write_weather_log()