import time
import logging
from fastapi import Request
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("gateway")

async def log_middleware(request: Request, call_next):
    start = time.time()
    resp = await call_next(request)
    cost = round((time.time() - start)*1000,2)
    client_ip = request.client.host if request.client else "unknown"
    logger.info(f"ip={client_ip} path={request.url.path} method={request.method} status={resp.status_code} cost={cost}ms")
    return resp
