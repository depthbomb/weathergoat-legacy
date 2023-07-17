from functools import cache
from src.store import redis
from datetime import datetime
from src.logger import logger
from disnake import Embed, Colour
from disnake.ext.tasks import loop
from disnake.ext.commands import Cog
from src.weathergoat import WeatherGoat
from src.utils import append_cache_buster
from src.models import AlertCollectionGeoJSON


class AlertsCog(Cog):
    _bot: WeatherGoat

    def __init__(self, bot: WeatherGoat):
        self._bot = bot

        self.report_alert.start()

    @loop(seconds=30)
    async def report_alert(self):
        await self._check_alerts()

    @report_alert.before_loop
    async def wait_until_ready(self) -> None:
        await self._bot.wait_until_ready()
        logger.debug("Alert loop is ready")

    async def _check_alerts(self) -> None:
        logger.debug("Checking alerts")

        zones = self._bot.config.alert_zones
        for zone in zones:
            channel_id = zone.channel_id
            zone_id = zone.zone_id
            radar_image = zone.radar_image
            channel = self._bot.get_channel(channel_id)

            if channel is None:
                logger.error("Could not find channel by ID %d" % channel_id)
                continue

            alert_endpoint = "https://api.weather.gov/alerts/active/zone/%s" % zone_id
            async with self._bot.httpclient.get(alert_endpoint) as res:
                if not res.ok:
                    logger.error("Failed to check alerts for zone %s: %s" % (zone_id, res.reason))
                    continue

                try:
                    res_data = await res.json()
                    alert_collection = AlertCollectionGeoJSON(**res_data)
                    features = alert_collection.features
                    if len(features) == 0:
                        logger.debug("No alerts for %s" % zone_id)
                        continue

                    feature = features[0]
                    alert = feature.properties
                    alert_id = alert.id
                    if redis.exists(alert_id):
                        logger.debug("Alert %s has already been reported" % alert_id)
                        continue

                    alert_expires = datetime.fromisoformat(alert.expires)

                    embed = Embed(
                            title=alert.headline,
                            description=f"```md\n{alert.description}```",
                            timestamp=datetime.now(),
                            color=self._get_severity_color(alert.severity)
                    )
                    embed.set_image(append_cache_buster(radar_image))
                    embed.add_field("Certainty", alert.certainty, inline=True)
                    embed.add_field("Effective Until", alert_expires.strftime("%c"), inline=True)
                    embed.add_field("Affected Areas", alert.area_description, inline=False)
                    embed.set_footer(text=alert.event)

                    if alert.instruction is not None:
                        embed.add_field("Instructions", alert.instruction, inline=False)

                    await channel.send(embed=embed)

                    redis.set(alert_id, "", ex=60*60*8)

                    logger.success("Reported alert %s to channel %d" % (alert_id, channel_id))
                except Exception as e:
                    logger.exception("Failed to parse response", e)

    @cache
    def _get_severity_color(self, severity: str) -> Colour:
        match severity:
            case "Extreme":
                color = 185, 28, 28
            case "Severe":
                color = 220, 38, 38
            case "Moderate":
                color = 249, 115, 22
            case "Minor":
                color = 253, 224, 71
            case _:
                color = 253, 224, 71

        return Colour.from_rgb(color[0], color[1], color[2])
