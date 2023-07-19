from aiohttp import ClientSession
from src.constants import USER_AGENT


def create_session() -> ClientSession:
    sess = ClientSession()
    sess.headers.update({"user-agent": USER_AGENT})

    return sess
