import requests, os, configparser
import pandas as pd
import json

CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

def _write_weather_log():

    r = requests.get('https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=59.9&lon=10.8')

    weather_df = r.json()
    weather_df = pd.DataFrame(weather_df)
    weather_df.to_json(CURR_DIR_PATH + '/data/weather-output.json', index=False)

_write_weather_log()

def _write_weather_log2():


    weather_df = pd.DataFrame(r)
    weather_df.to_json(CURR_DIR_PATH + '/weather-output.json', index=False)

def _fetch_weather_api_sweden(lat: float, lon: float) -> str:
    return f'https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/{lon}/lat/{lat}/data.json'
        
def _get_requests_api_weather(api_call: function) -> requests:
    return requests.get(api_call)


    


