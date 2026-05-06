import hashlib
import redis

# =========================
# REDIS CLIENT
# =========================

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

# =========================
# CACHE TTL
# =========================

CACHE_TTL = 3600

# =========================
# CACHE KEY
# =========================

def build_cache_key(
    namespace: str,
    *parts
):

    raw_key = "|".join(
        str(part).strip().lower()
        for part in parts
    )

    digest = hashlib.sha256(
        raw_key.encode("utf-8")
    ).hexdigest()

    return f"{namespace}:{digest}"

# =========================
# GET CACHE
# =========================

def get_cached_response(prompt: str):

    try:

        cached_response = redis_client.get(prompt)

        return cached_response

    except redis.RedisError:

        return None

# =========================
# SET CACHE
# =========================

def cache_response(
    prompt: str,
    response: str
):

    try:

        redis_client.setex(
            prompt,
            CACHE_TTL,
            response
        )

    except redis.RedisError:

        return
