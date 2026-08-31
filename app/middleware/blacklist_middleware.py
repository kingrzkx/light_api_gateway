from fastapi import Request, Response
from app.config import cfg

async def ip_blacklist_middleware(request: Request, call_next):
    ip = request.client.host if request.client else ""
    if ip in cfg.ip_filter.blacklist:
        return Response(content="ip forbidden", status_code=403)
    resp = await call_next(request)
    return resp
