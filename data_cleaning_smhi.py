import pandas as pd

weather_data = pd.read_json('data/weather_output_smhi.json')

def process_weather_data(weather_data, city_name):
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

    smhi_city_df_pivot = smhi_city_df_pivot[['time', 'air_pressure_at_sea_level','air_temperature','cloud_area_fraction','relative_humidity','wind_from_direction','wind_speed','next_1_hours_precipitation_amount']]

    smhi_city_df_pivot.to_csv(f'data/{city_lower}_smhi.csv', index=False)


process_weather_data(weather_data, 'Stockholm')
process_weather_data(weather_data, 'Oslo')


