from redis.client import Redis
from src.constants import DEBUG

__host = "localhost" if DEBUG else "cache"

redis = Redis(host=__host, port=6379, decode_responses=True)
