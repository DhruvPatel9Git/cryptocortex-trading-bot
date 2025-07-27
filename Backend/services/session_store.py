import json
from datetime import datetime, timedelta, timezone
from services.redis_client import redis_client
from models import Cache

async def store_session(user_id: str, data: dict, expiry_minutes: int):
    redis_key = f"user_session:{user_id}"
    expiry_seconds = expiry_minutes * 60

    redis_client.setex(redis_key, expiry_seconds, json.dumps(data))

    expires_at = datetime.now(timezone.utc) + timedelta(seconds=expiry_seconds)
    existing = await Cache.find_one(Cache.key == redis_key)
    if existing:
        existing.value = data
        existing.expires_at = expires_at
        await existing.save()
    else:
        await Cache(
            key=redis_key,
            value=data,
            expires_at=expires_at
        ).insert()

async def get_session(user_id: str):
    redis_key = f"user_session:{user_id}"
    # ✅ Check Redis first
    session_data = redis_client.get(redis_key)
    if session_data:
        return json.loads(session_data)


    doc = await Cache.find_one(Cache.key == redis_key)
    if doc and doc.expires_at > datetime.now(timezone.utc):
        ttl = int((doc.expires_at - datetime.now(timezone.utc)).total_seconds())
        redis_client.setex(redis_key, ttl, json.dumps(doc.value))
        return doc.value

    return None