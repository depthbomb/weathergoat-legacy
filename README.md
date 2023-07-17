# WeatherGoat

_WeatherGoat_ is my personal Discord bot for reporting weather forecasts and alerts to my server. It uses the [National Weather Service API](https://www.weather.gov/documentation/services-web-api), is built with Python (Disnake) and Redis, and runs in a Docker container.

## Setup

Create a `config.toml` file in the root directory:

```toml
[weathergoat]
# The user ID that owns this bot
owner_id = 123

[cleanup]
# The cron expression that determines when to delete previously sent messages
schedule = "0 5 * * *"
# The timezone to use alongside the aforementioned cron expression
# See `all_timezones` in the `pytz` package
timezone = "US/Eastern"
# Channel IDs to delete messages in daily, normally set to the alert and forecast channels to keep them tidy
# Set to an empty array (channel_ids = []) to disable cleanup
channel_ids = [456, 789]

[forecast]
# The cron expression that determines when a forecast report will be sent
# For example use "0 8,13,19 * * *" to report at 8AM, 1PM, and 7PM
cron_expression = "0 13 * * *"
# The timezone to use alongside the aforementioned cron expression
# See `all_timezones` in the `pytz` package
timezone = "US/Eastern"

[[alert_zones]]
# Channel ID to report alerts to
channel_id = 456
# The "zone ID" of the location to check alerts for - see https://www.weather.gov/media/documentation/docs/NWS_Geolocation.pdf
zone_id = "..."
# Find radar images at https://radar.weather.gov/ridge/standard/
radar_image = "https://radar.weather.gov/ridge/standard/..."

[[forecast_zones]]
# Channel ID to send daily forecasts to
channel_id = 789
# Approximate latitude of the area to get the forecast for
latitude = 12.34
# Approximate longitude of the area to get the forecast for
longitude = -56.78
# Find radar images at https://radar.weather.gov/ridge/standard/
radar_image = "https://radar.weather.gov/ridge/standard/..."
```


## Running

Start `main.py` with a `TOKEN` environment variable containing your bot's token.
