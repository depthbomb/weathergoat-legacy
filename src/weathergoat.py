from datetime import datetime
from src.logger import logger
from src.config import config
from aiohttp import ClientSession
from humanize import naturaldelta
from disnake.ext.tasks import loop
from src.constants import USER_AGENT
from disnake.ext.commands import InteractionBot
from disnake import Status, Intents, Activity, ActivityType


class WeatherGoat(InteractionBot):
    _start: datetime = datetime.now()

    httpclient: ClientSession

    def __init__(self):
        super().__init__(
                owner_id=config.weathergoat.owner_id,
                intents=Intents(guilds=True, guild_messages=True, members=True)
        )

        self.httpclient = ClientSession()
        self.httpclient.headers.update({"user-agent": USER_AGENT})

        self._update_uptime_status.start()

    async def on_ready(self):
        logger.success("Ready to serve %d member(s) in %d guild(s)" % (len(self.users), len(self.guilds)))

    @loop(seconds=15.0)
    async def _update_uptime_status(self):
        await self.wait_until_ready()

        delta = naturaldelta(datetime.now() - self._start)
        await self.change_presence(
                status=Status.dnd,
                activity=Activity(
                        name=f"the weather for {delta}",
                        type=ActivityType.watching
                )
        )
