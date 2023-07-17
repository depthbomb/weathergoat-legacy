from os import getenv
from pathlib import Path

DEBUG = getenv("DEBUG", True)

VERSION = (2, 0, 0)
VERSION_STRING = [".".join(str(v)) for v in VERSION]

USER_AGENT = f"WeatherGoat v{VERSION_STRING} (github.com/depthbomb/weathergoat)"

ROOT_DIR = Path(".").resolve()
CONFIG_PATH = ROOT_DIR / "config.toml"
