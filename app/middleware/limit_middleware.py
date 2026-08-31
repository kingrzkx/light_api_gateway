from fastapi import Request, Response
from app.config import cfg
from app.utils import redis_client

async def rate_limit_middleware(request: Request, call_next):
    if not cfg.rate_limit.enable:
        return await call_next(request)

    ip = request.client.host if request.client else "unknown"
    key = f"rate:ip:{ip}"
    count = redis_client.incr(key)
    if count == 1:
        redis_client.expire(key, cfg.rate_limit.expire_seconds)

    if count > cfg.rate_limit.per_ip_max:
        return Response(content="too many requests", status_code=429)

    resp = await call_next(request)
    return resp
