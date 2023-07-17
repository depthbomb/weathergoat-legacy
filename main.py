from os import getenv
from src.store import redis
from src.logger import logger
from src.cogs.alerts import AlertsCog
from src.weathergoat import WeatherGoat
from src.cogs.cleanup import CleanupCog
from src.cogs.forecast import ForecastCog

if __name__ == '__main__':
    logger.info("Starting up")

    wg = WeatherGoat()
    wg.add_cog(CleanupCog(wg))
    wg.add_cog(AlertsCog(wg))
    wg.add_cog(ForecastCog(wg))
    wg.run(getenv("TOKEN"))

    redis.close()
