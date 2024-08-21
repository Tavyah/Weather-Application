CREATE TABLE IF NOT EXISTS weather_data (
	id SERIAL PRIMARY KEY,
	time VARCHAR(30),
    air_pressure_at_sea_level DECIMAL,
    air_temperature DECIMAL,
    cloud_area_fraction DECIMAL,
    relative_humidity DECIMAL,
    wind_from_direction DECIMAL,
    wind_speed DECIMAL,
    next_1_hours_precipitation_amount DECIMAL
);

INSERT INTO weather_data (time, air_pressure_at_sea_level, air_temperature,cloud_area_fraction,relative_humidity,wind_from_direction,wind_speed,next_1_hours_precipitation_amount)
VALUES ();

SELECT * FROM weather_data;