import pandas as pd

weather_data_met = pd.read_json('data/weather_output_met.json')
weather_data_smhi = pd.read_json('data/weather_output_smhi.json')

def process_met_weather_data(weather_data, city_name):
    city_lower = city_name.lower()

    city_data = weather_data[weather_data['city'] == city_name].iloc[0]

    #Create a dict of the weather data specifically (no need for coordinates etc.)
    weather_data_dict = city_data['weather_data']

    #List of what is further down the hierarchy (properties -> timeseries)
    timeseries = weather_data_dict['properties']['timeseries']

    #normalize/flatten data structure
    city_df = pd.json_normalize(timeseries)

    #get rid of all columns containing 'symbol_code' as it is not relevant for db
    city_df_mod = city_df[city_df.columns.drop(list(city_df.filter(regex='symbol_code')))]

    #drop precipitation data for next 6 hours for each time in timeseries, as we only need next 1 hour
    city_df_mod.drop(columns=['data.next_6_hours.details.precipitation_amount'], inplace=True)

    #rename columns to shorten long names from the normalization (remove data, instant and details cats from name)
    city_df_mod.columns = city_df_mod.columns.str.replace('data.instant.details.', '')
    city_df_mod.rename(columns={'data.next_1_hours.details.precipitation_amount': 'next_1_hours_precipitation_amount'}, inplace=True)

    #only want 24h cycle
    city_df_mod = city_df_mod.head(24)

    #decimal precision of 1
    city_df_mod = city_df_mod.round(1)

    city_df_mod.to_csv(f'data/{city_lower}_met.csv', index=False)

def process_smhi_weather_data(weather_data, city_name):
    city_lower = city_name.lower()
    
    city_data = weather_data[weather_data['city'] == city_name].iloc[0]
 
    city_data_dict=city_data['weather_data']['timeSeries']

    smhi_city_df=pd.json_normalize(city_data_dict)

    exploded = smhi_city_df.explode('parameters')
    smhi_city_df_mod = pd.concat([exploded['validTime'].reset_index(drop=True), pd.json_normalize(exploded['parameters'])], axis=1)

    smhi_city_df_mod['values'] = smhi_city_df_mod['values'].str[0]

    smhi_city_df_pivot = smhi_city_df_mod.pivot(index='validTime', columns='name', values='values').reset_index()
    smhi_city_df_pivot = smhi_city_df_pivot.head(24)

    smhi_city_df_pivot = smhi_city_df_pivot.drop(columns=['gust', 'lcc_mean', 'mcc_mean', 'hcc_mean', 'spp', 'pcat', 'pmin', 'pmax', 'vis', 'pmedian', 'Wsymb2', 'tstm'])

    smhi_city_df_pivot = smhi_city_df_pivot.rename(columns={'tcc_mean': 'cloud_area_fraction', 'msl': 'air_pressure_at_sea_level',
        'r': 'relative_humidity', 'ws': 'wind_speed', 'wd': 'wind_from_direction', 't': 'air_temperature', 
        'pmean': 'next_1_hours_precipitation_amount', 'validTime': 'time'})

    smhi_city_df_pivot = smhi_city_df_pivot.round(1)

    #convert from oktas to percent
    smhi_city_df_pivot['cloud_area_fraction'] = smhi_city_df_pivot['cloud_area_fraction'] * 12.25

    smhi_city_df_pivot = smhi_city_df_pivot[['time', 'air_pressure_at_sea_level','air_temperature','cloud_area_fraction','relative_humidity','wind_from_direction','wind_speed','next_1_hours_precipitation_amount']]

    smhi_city_df_pivot.to_csv(f'data/{city_lower}_smhi.csv', index=False)


process_smhi_weather_data(weather_data_smhi, 'Stockholm')
process_smhi_weather_data(weather_data_smhi, 'Oslo')

process_met_weather_data(weather_data_met, 'Oslo')
process_met_weather_data(weather_data_met, 'Stockholm')