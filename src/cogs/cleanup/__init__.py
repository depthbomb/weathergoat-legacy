from pytz import timezone
from aiocron import crontab
from src.logger import logger
from disnake.ext.commands import Cog
from src.weathergoat import WeatherGoat


class CleanupCog(Cog):
    _bot: WeatherGoat
    _channels: list[int]

    def __init__(self, bot: WeatherGoat):
        self._bot = bot
        self._channels = self._bot.config.cleanup.channel_ids

        tz = timezone(self._bot.config.cleanup.timezone)

        crontab(self._bot.config.cleanup.schedule, self.do_cleanup, tz=tz)

    async def do_cleanup(self):
        await self._bot.wait_until_ready()
        if len(self._channels) == 0:
            return

        total_deleted_message = 0
        for id_ in self._channels:
            channel = self._bot.get_channel(id_)
            deleted_messages = await channel.purge()
            num_deleted_messages = len(deleted_messages)
            total_deleted_message += num_deleted_messages
            logger.success("Cleaned up %d message(s) in channel %d" % (num_deleted_messages, id_))

        logger.success("Cleaned up %d message(s) in %d channel(s)" % (total_deleted_message, len(self._channels)))
