from tomllib import loads
from functools import cache
from src.models import Config
from src.constants import CONFIG_PATH


@cache
def load_config() -> Config:
    with CONFIG_PATH.open("r", encoding="utf8") as file:
        cfg = loads(file.read())
        return Config(**cfg)


config = load_config()
