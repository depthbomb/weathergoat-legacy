import re
import random
import string
import requests
from cache import cache
from config import config
from logger import logger


class Weather:
    webhook_url: str = config["discord"]["webhook_url"]
    image_url: str = config["discord"]["image"]
    headers: dict[str, str] = {"user-agent": "weathergoat"}

    def check_zone(self, zone: str) -> None:
        logger.info("Checking zone %s", zone)
        res = requests.get(f"https://api.weather.gov/alerts?zone={zone}", headers=self.headers)
        if not res.ok:
            logger.error("Response failed: %d - %s", res.status_code, res.reason)
            return

        json = res.json()
        features = json["features"]

        if len(features) == 0:
            logger.info("No alerts")
            return

        latest_alert = features[0]["properties"]
        alert_id = latest_alert["id"]
        alert_type = latest_alert["event"]
        alert_areas = latest_alert["areaDesc"]
        alert_expires = latest_alert["expires"]
        alert_severity = latest_alert["severity"]
        alert_headline = latest_alert["headline"]
        alert_description = re.sub(r"(\\n\\n|\\n)", " ", latest_alert["description"])

        if str.startswith(alert_type, "Flood"):
            logger.info("Ignoring flood event")
            return

        if cache.has_item(alert_id):
            logger.debug("Alert has already been broadcast")
            return

        self.send_webhook(
            areas=alert_areas,
            severity=alert_severity,
            headline=alert_headline,
            description=alert_description,
            expires=alert_expires
        )
        logger.info("Sent alert for %s", alert_id)
        cache.add_item(alert_id, json)

    @staticmethod
    def get_severity_color(severity: str) -> int:
        match severity:
            case 'Severe':
                color = config["discord"]["color_severe"]
            case 'Moderate':
                color = config["discord"]["color_moderate"]
            case _:
                color = config["discord"]["color_minor"]

        return int(color)

    def send_webhook(self, areas: str, severity: str, headline: str, description: str, expires: str) -> None:
        username = config["discord"]["username"]
        avatar = config["discord"]["avatar"]
        data = {
            "username": username,
            "avatar_url": avatar,
            "embeds": [{
                "title": headline,
                "color": self.get_severity_color(severity),
                "description": f"```{description}```",
                "image": {
                    "url": self.__get_radar_image()
                },
                "fields": [
                    {
                        "name": "Affected Areas",
                        "value": areas
                    },
                    {
                        "name": "Effective Until",
                        "value": expires
                    }
                ]
            }]
        }
        res = requests.post(self.webhook_url, headers=self.headers, json=data)
        logger.info("Sent webhook") if res.ok else logger.error("Failed to send webhook: %d - %s - %s", res.status_code,
                                                                res.reason, res.text)

    def __get_radar_image(self) -> str:
        cache_buster = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        return f"{self.image_url}?v={cache_buster}"
