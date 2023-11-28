units: str ="metric"

max_days_forecast: int = 7

max_days_history: int = 7

# needs to update the current weather with the first request if 60 minutes have passed since the last update of the current weather.
time_to_update_current_weather: int = 60