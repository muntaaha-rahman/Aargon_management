import redis
from .settings import settings
from datetime import timedelta

redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

#for storiong revoked token
def store_revoked_token(jti: str, ttl: timedelta):
    redis_client.setex(name=jti, time=int(ttl.total_seconds()), value="revoked")

#check revoked token
def is_token_revoked(jti: str) -> bool:
    return redis_client.exists(jti) == 1