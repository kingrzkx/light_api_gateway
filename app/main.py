from fastapi import FastAPI
from app.config import cfg
from app.proxy import proxy_request
from app.middleware.log_middleware import log_middleware
from app.middleware.blacklist_middleware import ip_blacklist_middleware
from app.middleware.auth_middleware import auth_middleware
from app.middleware.limit_middleware import rate_limit_middleware
from fastapi import FastAPI, Request

app = FastAPI(title="Light‑API‑Gateway", version="1.0.0")

# 注册中间件，顺序很重要：日志最先执行，然后黑名单、限流、鉴权
@app.middleware("http")
async def log_mw(request, call_next):
    return await log_middleware(request, call_next)

@app.middleware("http")
async def black_mw(request, call_next):
    return await ip_blacklist_middleware(request, call_next)

@app.middleware("http")
async def limit_mw(request, call_next):
    return await rate_limit_middleware(request, call_next)

@app.middleware("http")
async def auth_mw(request, call_next):
    return await auth_middleware(request, call_next)

# 健康检查接口，配置中设置无需鉴权
@app.get("/gateway/health")
async def health():
    return {"status":"ok","service":"light‑api‑gateway"}

# 所有其它路径全部转发到后端服务
@app.api_route("/{path:path}", methods=["GET","POST","PUT","DELETE","PATCH","OPTIONS"])
async def gateway_all(path: str, request: Request):
    return await proxy_request(request)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=cfg.gateway.host, port=cfg.gateway.port)
