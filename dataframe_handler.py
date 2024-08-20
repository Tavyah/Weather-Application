import pandas as pd
import os

def get_name(api_call: list) -> str:
    filepath = _get_filepath(api_call)
    base_name = os.path.basename(filepath)
    return base_name.split('_')[0]

def get_dataframe(api_call: list) -> pd.DataFrame:
    filepath = _get_filepath(api_call)
    # TODO: Error handling
    return pd.read_csv(filepath)

def _get_filepath(api_call: list) -> os: # TODO input filename
    current_dir = os.path.dirname(os.path.realpath(__file__))
    data_folder = 'data'
    filename = ''
    if 'MET' in api_call:
        filename = 'oslo_met.csv'
    if 'SMHI' in api_call:
        filename = 'oslo_smhi.csv'
    return os.path.join(current_dir, data_folder, filename)

def get_date(api_call: list) -> str:
    df = get_dataframe(api_call)
    date_start, _ = df['time'].iloc[0].split('T') # TODO: Error handling if string doesnt have T to split on
    date_end, _ = df['time'].iloc[-1].split('T')
    return f'{date_start} - {date_end}' if date_start != date_end else date_start