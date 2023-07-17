from aiocron import crontab
from functools import cache
from datetime import datetime
from src.logger import logger
from disnake import Embed, Colour
from disnake.ext.commands import Cog
from src.weathergoat import WeatherGoat
from src.utils import append_cache_buster
from src.models import PointGeoJSON, GridpointForecastGeoJSON


class ForecastCog(Cog):
    _bot: WeatherGoat

    def __init__(self, bot: WeatherGoat):
        self._bot = bot

        crontab("0 8,13,19 * * *", self.report_forecast)

    async def report_forecast(self):
        await self._bot.wait_until_ready()

        zones = self._bot.config.forecast_zones
        for zone in zones:
            channel = self._bot.get_channel(zone.channel_id)
            lat = zone.latitude
            lon = zone.longitude
            if channel is None:
                logger.error("Could not find forecast channel by ID %d" % zone["channel_id"])
                continue

            location, forecast_url = await self._get_coordinate_info(lat, lon)
            async with self._bot.httpclient.get(forecast_url) as res:
                if not res.ok:
                    logger.error("Failed to retrieve forecast data from %s: %s" % (forecast_url, res.reason))
                    continue

                json = await res.json()
                data = GridpointForecastGeoJSON(**json)

                periods = data.properties.periods
                forecast = periods[0]
                time = forecast.name  # The name of the period is the time of day
                icon = str(forecast.icon).replace("medium", "large")
                short_forecast = forecast.short_forecast
                detailed_forecast = forecast.detailed_forecast

                embed = Embed(
                        title=f"{time}'s Forecast for {location}",
                        description=detailed_forecast,
                        color=Colour.blue(),
                        timestamp=datetime.now()
                )
                embed.set_thumbnail(url=icon)
                embed.set_image(url=append_cache_buster(zone.radar_image))
                embed.add_field("At a glance", short_forecast, inline=False)

                await channel.send(embed=embed)

                logger.success("Successfully reported forecast for %s" % location)

    @cache
    async def _get_coordinate_info(self, lat: float, lon: float) -> tuple[str, str]:
        key = f"{lat},{lon}"

        logger.debug("Retrieving info from coordinates %s" % key)

        async with self._bot.httpclient.get(f"https://api.weather.gov/points/{key}") as res:
            if not res.ok:
                raise Exception(res.reason)

            json = await res.json()
            data = PointGeoJSON(**json)
            location = data.properties.relative_location.properties
            city = location.city
            state = location.state
            coordinates_location = f"{city}, {state}"
            forecast_url = data.properties.forecast

            return coordinates_location, forecast_url
