def _units_met() -> dict:
  return {
          "air_pressure_at_sea_level": "hPa",
          "air_temperature": "celsius",
          "cloud_area_fraction": "%",
          "precipitation_amount": "mm",
          "relative_humidity": "%",
          "wind_from_direction": "degrees",
          "wind_speed": "m/s"
  }

def unit(weather_parameter: str) -> str:
  units = _units_met()
  return units.get(weather_parameter, 'Unknown unit') # If the unit doesn't exist, it will return "unknown unit" otherwise it will return the unit.