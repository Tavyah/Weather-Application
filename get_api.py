import extract_data as get_from_api
import harmonization

def api_data() -> None:
    get_from_api._write_weather_log('smhi')
    get_from_api._write_weather_log('met')
    harmonization.process_met_weather_data('Oslo')
    harmonization.process_met_weather_data('Stockholm')
    harmonization.process_smhi_weather_data('Oslo')
    harmonization.process_smhi_weather_data('Stockholm')