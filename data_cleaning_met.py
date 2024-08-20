import pandas as pd

#divide weather data based on city
weather_data = pd.read_json('data/weather_output_met.json')
weather_data_oslo = weather_data[weather_data['city'] == 'Oslo']
weather_data_stockholm = weather_data[weather_data['city'] == 'Stockholm']

#Access the data under each city
weather_data_oslo = weather_data_oslo.iloc[0]
weather_data_stockholm = weather_data_stockholm.iloc[0]

#Create a dict of the weather data specifically (no need for coordinates etc.)
weather_data_oslo_dict = weather_data_oslo['weather_data']
weather_data_stockholm_dict = weather_data_stockholm['weather_data']

#List of what is further down the hierarchy (properties -> timeseries)
timeseries_oslo = weather_data_oslo_dict['properties']['timeseries']
timeseries_stockholm = weather_data_stockholm_dict['properties']['timeseries']

#normalize/flatten data structure
oslo_df = pd.json_normalize(timeseries_oslo)
stockholm_df = pd.json_normalize(timeseries_stockholm)

#get rid of all columns containing 'symbol_code' as it is not relevant for db
oslo_df_mod = oslo_df[oslo_df.columns.drop(list(oslo_df.filter(regex='symbol_code')))]
stockholm_df_mod = stockholm_df[stockholm_df.columns.drop(list(stockholm_df.filter(regex='symbol_code')))]

#drop precipitation data for next 6 hours for each time in timeseries, as we only need next 1 hour
oslo_df_mod.drop(columns=['data.next_6_hours.details.precipitation_amount'], inplace=True)
stockholm_df_mod.drop(columns=['data.next_6_hours.details.precipitation_amount'], inplace=True)

#rename columns to shorten long names from the normalization (remove data, instant and details cats from name)
oslo_df_mod.columns = oslo_df_mod.columns.str.replace('data.instant.details.', '')
stockholm_df_mod.columns = stockholm_df_mod.columns.str.replace('data.instant.details.', '')
oslo_df_mod.rename(columns={'data.next_1_hours.details.precipitation_amount': 'next_1_hours_precipitation_amount'}, inplace=True)
stockholm_df_mod.rename(columns={'data.next_1_hours.details.precipitation_amount': 'next_1_hours_precipitation_amount'}, inplace=True)

#only want 24h cycle
oslo_df_mod = oslo_df_mod.head(24)
stockholm_df_mod = stockholm_df_mod.head(24)

#decimal precision of 1
oslo_df_mod = oslo_df_mod.round(1)
stockholm_df_mod = stockholm_df_mod.round(1)

oslo_df_mod.to_csv('data/oslo_met.csv', index=False)
stockholm_df_mod.to_csv('data/stockholm_met.csv', index=False)