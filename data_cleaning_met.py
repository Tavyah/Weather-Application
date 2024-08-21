import pandas as pd

#divide weather data based on city
weather_data = pd.read_json('data/weather_output_met.json')

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


process_met_weather_data(weather_data, 'Oslo')
process_met_weather_data(weather_data, 'Stockholm')