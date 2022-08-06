import time
import schedule
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

    check_weather_alerts()

    interval = int(config["weather"]["check_interval"])
    should_loop = True
    job = schedule.every(interval).minutes.do(check_weather_alerts)
    while should_loop:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Stopping job")
            should_loop = False
            schedule.cancel_job(job)
            pass

    exit(0)
