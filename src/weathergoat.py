from disnake import Intents
from src.logger import logger
from src.config import config
from aiohttp import ClientSession
from src.constants import USER_AGENT
from disnake.ext.commands import InteractionBot


class WeatherGoat(InteractionBot):
    httpclient: ClientSession

    def __init__(self):
        super().__init__(
                owner_id=config.weathergoat.owner_id,
                intents=Intents(guilds=True, guild_messages=True, members=True)
        )

        self.httpclient = ClientSession()
        self.httpclient.headers.update({"user-agent": USER_AGENT})

    async def on_ready(self):
        logger.success("Ready to serve %d member(s) in %d guild(s)" % (len(self.users), len(self.guilds)))
