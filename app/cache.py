import os
import redis

REDIS_URL = os.environ["REDIS_URL"]

# decode_responses=True → on récupère des str, pas des bytes
r = redis.from_url(REDIS_URL, decode_responses=True)

TTL_SECONDS = 3600  # le cache expire au bout d'1h


def get_cached_url(code: str) -> str | None:
    return r.get(f"link:{code}")


def set_cached_url(code: str, url: str) -> None:
    r.setex(f"link:{code}", TTL_SECONDS, url)


def invalidate(code: str) -> None:
    r.delete(f"link:{code}")