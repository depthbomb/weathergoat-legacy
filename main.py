from os import getenv
from sentry_sdk import init
from src.store import redis
from src.logger import logger
from src.config import config
from src.cogs.alerts import AlertsCog
from src.weathergoat import WeatherGoat
from src.cogs.cleanup import CleanupCog
from src.cogs.forecast import ForecastCog

if __name__ == '__main__':
    logger.info("Starting up")

    if config.sentry.dsn is not None or config.sentry.dsn != "":
        init(dsn=config.sentry.dsn)

    wg = WeatherGoat()
    wg.add_cog(CleanupCog(wg))
    wg.add_cog(AlertsCog(wg))
    wg.add_cog(ForecastCog(wg))
    wg.run(getenv("TOKEN"))

    redis.close()
