from random import choices
from string import ascii_letters
from urllib.parse import urlparse


def append_cache_buster(url: str) -> str:
    buster = "".join(choices(ascii_letters+"_-", k=64))
    return f"{url}?{buster}"


def is_url_valid(url: str) -> bool:
    try:
        r = urlparse(url)
        return all([r.scheme, r.netloc])
    except:
        return False
