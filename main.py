import time
from sys import exit
from logger import logger
from config import config
from weather import Weather

weather = Weather()


def check_weather_alerts() -> None:
    zones = config["weather"]["zones"].split(",")
    [weather.check_zone(zone) for zone in zones]


if __name__ == "__main__":
    logger.info("Starting")

    interval = int(config["weather"]["check_interval"])
    should_loop = True
    while should_loop:
        try:
            check_weather_alerts()
            time.sleep(interval)
        except KeyboardInterrupt:
            should_loop = False

    exit(0)
