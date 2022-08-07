from urllib import parse
from logger import logger
from os import path, makedirs
from appdirs import user_cache_dir


class Cache:
    log: logger
    cache_dir: str

    def __init__(self) -> None:
        self.log = logger
        self.cache_dir = user_cache_dir(appname="weathergoat", appauthor="Caprine Logic")
        makedirs(self.cache_dir) if not path.exists(self.cache_dir) else None

    def has_item(self, identifier: str) -> bool:
        """Returns True if an item exists in the cache."""
        return path.exists(self.__get_item_path(identifier))

    def add_item(self, identifier: str, value: dict) -> None:
        """Adds an item to the cache."""
        if not self.has_item(identifier):
            try:
                with open(self.__get_item_path(identifier), "a") as item:
                    item.write(str(value))
            except IOError:
                self.log.exception("Failed to write cache item", exc_info=True)

    def __get_item_path(self, identifier: str) -> str:
        return path.join(self.cache_dir, parse.quote(identifier))


cache = Cache()
